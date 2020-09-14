
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project:  Generar una estrategia de inversion para un capital de 1,000,000 de pesos                                                      -- #
# -- script: data.py : script que guarda las variables de los datos utilizados                                                 -- #
# -- author: elvi7bello                                                                                   -- #
# -- license: GPL-3.0 License                                                                             -- #
# -- repository: https://github.com/elvi7bello/myst_lab1_EBA                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

#DATA.PY: Entrada y salida de datos

import pandas as pd
from os import listdir, path
from os.path import isfile, join
import numpy as np
import yfinance as yf
import time as time

pd.set_option('display.max_rows', None)            #sin limite de renglones maximos
pd.set_option('display.max_columns', None)         #sin limite de columnas maximas
pd.set_option('display.width', None)               #sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)  #visualizar todas las columnnas

#---------------------------------------------------------------------------------------------- Paso 1.1
 #----Obtener la lista de los archivos a leer

#Obtener la ruta absoluta de la carpeta donde estan los archivos
abspath = path.abspath('files/NAFTRAC_holdings')
#Obtener una lista de todos los archivos en la carpeta (quitandole la extensión del archivo)
#No tener los archivos abiertos al mismo tiempo de correr la siguiente linea, sino seria error "loc.archivo"
archivos = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))] #comprension de lista
archivos = ['NAFTRAC_' + i.strftime('%d%m%y') for i in sorted(pd.to_datetime(archivos))]

#----------------------------------------------------------------------------------------------- Paso 1.2
# -- Leer todos los archivos y guardarlos en un diccionario

#Crear un diccionario para almacenar todos los datos
data_archivos = {}
for i in archivos:
   # i = archivos[0]

    #leer archivo desde los 2 primeros renglones
    data = pd.read_csv('files/NAFTRAC_holdings/'+ i + '.csv', skiprows=2, header=None)
    #renombrar las columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    #Quitar columnas que no sean nan
    data = data.iloc[:, pd.notnull(data.columns)]
    #rastrear el indice
    data= data.iloc[1:-1].reset_index(drop=True, inplace=False)
    #Quitar las comas en la columna de precios
    data['Precio'] = [i.replace(',', '') for i in data['Precio']]
    #Quitar * a la columna de ticker
    data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
    #Hacer conversiones de tipos de columnas a numerico
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data=data.astype(convert_dict)
    #Convertir a decimal la columna de peso (%)
    data['Peso (%)'] = data['Peso (%)']/100
    #Guardar en diccionario
    data_archivos[i]=data

#----------------------------------------------------------------------------------------------- Paso 1.3
# -- Construir el vector de fechas a partir del vector de nombre de archivos

#etiquetas para dataframe y para yfinance
t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

#lista con fechas ordenadas (para usarse como indexadores de archivos)
i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

#----------------------------------------------------------------------------------------------- Paso 1.4
# -- Construir el vector de tickers utilizables en yahoo finance
tickers = []
for i in archivos:
    # i = archivos[0]
    l_tickers = list(data_archivos[i]["Ticker"])
    #print(l_tickers)
    [tickers.append(i + '.MX') for i in l_tickers]
global_tickers = np.unique(tickers).tolist()

#ajustes de nombre de tickers
global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

#Eliminar entradas de efectivo: MXN, USD, y tickers con prblemas de precios

[global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX']] #se mandara a cash


#----------------------------------------------------------------------------------------------- Paso 1.5
# -- Descargar y acomodar todos los precios historicos

#contar tiempo que tarda
inicio = time.time()

data = yf.download(global_tickers, start= "2018-01-30", end="2020-08-24", action=False,
                   group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)

#tiempo que se tarda
print('se tardo', round(time.time() - inicio, 2), 'segundos')

#convertir columna de fechas
data_close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers})

#Tomar solo las fechas de interes (utilizando teoria de conjuntos)
ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))

#localizar todos los precios
precios = data_close.iloc[[int(np.where(data_close.index == i)[0]) for i in ic_fechas]]

#ordenar columnas lexicograficamente
precio = precios.reindex(sorted(precios.columns), axis=1)

#----------------------------------------------------------------------------------------------- Paso 1.6
# -- Posicion inicial

#Capital inicial
k = 1000000
#comisiones por transaccion
c=0.00125
#vector de comisiones historicas
comisiones = []

#los % para KOFL, KOFUBL, BSMXB, USD asignarlos a cash
c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'USD', 'MXN']
#DICCIONARIO PARA RESULTADO FINAL - POSICION INICIAL
df_pasiva = {'timestamp': ['30-01-2018'], 'capital': [k]}

pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]

#extraer la lista de archivos a eliminar
i_activos = list(pos_datos[list(pos_datos['Ticker'].isin(c_activos))].index)
#eliminar los archivos del DataFrame
pos_datos.drop(i_activos, inplace=True)

#resetear el index
pos_datos.reset_index(inplace=True, drop=True)

#agregar .MX para empatar los precios
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'

#corregir los tickers en datos
pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')
pos_datos['Ticker']= pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')

# -- Desgloce ----------------------------------
match = 0
precios.index.to_list()[match]

#precios necesarios para la postura metodo 1
m1 = np.array(precios.iloc[match, [i in pos_datos['Ticker'].to_list() for i in precios.columns.to_list()]])
m2 = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]

pos_datos['Precio_m1'] = m1
pos_datos['Precio'] = m2

#capital destinado por accion = proporcion de capital - comisiones por la posicion
pos_datos['Capital'] = pos_datos['Peso (%)']*k - pos_datos['Peso (%)']*k*c

#Cantidad de titulos por accion
pos_datos['Titulos'] = pos_datos['Capital']//pos_datos['Precio']

#valor de la postura por accion
pos_datos['Postura'] = pos_datos['Titulos']*pos_datos['Precio']

#Comision pagada
pos_datos['Comision'] = pos_datos['Postura']*c
pos_comision = pos_datos['Comision'].sum()

#efectivo libre en la posicion
pos_cash = k -pos_datos['Postura'].sum() - pos_comision

#Valor de la posicion
pos_value = pos_datos['Postura'].sum()


## -- Evolucion de la posicion (Inversion pasiva) (para mandarlo a todos los meses)

df_pasiva = {'timestamp': ['30-01-2018'], 'Capital': [k]}

for arch in range(0, len(archivos)):

    #Actualizar la columna de precio en el mismo dataframe de acuerdo al valor de la postura
    precios.index.to_list()[arch]
    m2 = [precios.iloc[match, precios.columns.to_list().index(i)]
          for i in pos_datos['Ticker']]
    pos_datos['Precio'] = m2

    #Valor de la postura por accion
    pos_datos['Postura'] = pos_datos['Titulos']*pos_datos['Precio']

    #Valor de la postura
    pos_value = pos_datos['Postura'].sum()

    #actualizar lista de valores de cada llave en el diccionario
    df_pasiva['timestamp'].append(t_fechas[arch])
    df_pasiva['Capital'].append(pos_value + pos_cash)

    # empatar para que se vaya sumando uno
    match = match + 1

df_pasiva = pd.DataFrame(df_pasiva)

#rendimiento logaritmico por mes
df_pasiva['rend'] = [0] + list((df_pasiva['Capital']/df_pasiva['Capital'].shift(1))-1)[1:]
#redondeo del rendimiento
df_pasiva['rend'] = round(df_pasiva['rend'], 4)
#redondeo del capital
df_pasiva['Capital'] = round(df_pasiva['Capital'], 2)
#redondeo del rendimiento acumulado
df_pasiva['rend_acum'] = round(df_pasiva['rend'].cumsum(), 4)


