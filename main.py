
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Generar una estrategia de inversion para un capital de 1,000,000 de pesos                                                         -- #
# -- script: main.py : mandar llamar las funciones y codigos breves del acomodo de datos                 -- #
# -- author: elvis7bello                                                                                 -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/elvi7bello/myst_lab1_EBA                                             -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# MAIN.PY : Aqui va el codigo completo

import data as dt
import yfinance as yf
import functions as fn

#data.py
#---------------------------------------------------------------------------------------------------------- Paso 1.1
# -- Obtener la lista de los archivos a leer
archivos = dt.archivos

#mostrar los primeros 10 nombres de los archivos
print(archivos[0:9])

#data.py
#---------------------------------------------------------------------------------------------------------- Paso 1.2
# -- Leer todos los archivos y gurdarlos en un diccionario
data_archivos = dt.data_archivos

#mostrar las primeras 10 llaves
print(list(data_archivos.keys())[0:9])

#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.3
# -- Construir el vector de fechas a partir del vector de nombre de archivos
fechas = fn.f_fechas(p_archivos = archivos)

#mostrar las primeras 10 columnas (con formato 1)
print(fechas['i_fechas'][0:9])

#mostrar las primeras 10 fechas (con formato 2)
print(fechas['t_fechas'][0:9])

#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.4
# -- Construir el vector de tickers utilizables en yahoo finance

global_tickers = fn.f_tickers(p_archivos=archivos, p_data_archivos=data_archivos)

#mostrar los tickers globales (10)
print(global_tickers[0:9])

#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.5
# -- Descargar y acomodar todos los precios historicos

precios = fn.f_obtener_precios(p_tickers=global_tickers, p_fechas = fechas['i_fechas'])
precios = precios ['Precios']

#mostrar los primeros 5 precios
print(precios.head(5))

#main.py
#---------------------------------------------------------------------------------------------------------- Paso 1.6
# -- Posicion inicial

k = 1000000 #capital inicial
c = 0.00125 #comision por operacion (0.125%)
params = {'k': k, 'c':c, 'fecha_ini': '2018'}

pos_ini = fn.f_pos_i(p_data_archivos=data_archivos, p_arhivo_ini = dt.archivos[0],
                     p_precios = precios, p_params=params)

#mostrar dataframe con la posicion inicial (solo los primeros 5 renglones)
print(pos_ini['pos_datos'].head(10))

#mostrar el efectivo sobrante en la postura inicial
print(pos_ini['pos_cash'])

#mostrar el valor de postura inicial
print(pos_ini['pos_value'])

#main.py
#---------------------------------------------------------------------------------------------------------- Paso 1.7
# -- Evolucion de la posicion (inversion pasiva)
df_inv_pasiva = fn.f_pasiva(p_fechas = fechas, p_archivos=archivos, p_precios=precios, p_pos_ini = pos_ini,
                            p_params = params)

#mostrar el dataframe de la evolucion del capital (los primeros 10 renglones)
print(df_inv_pasiva.head(10))


# main.py
#---------------------------------------------------------------------------------------------------------- Paso 1.8
# -- INVERSION ACTIVA

#evolucion de la postura

#mostrar un dataframe con evolucion de capital (los primeros 10 renglones)

#mostrar un dataframe con el historico de operaciones (los primeros 10 renglones)

# main.py
#---------------------------------------------------------------------------------------------------------- Paso 1.9
# -- medidas de atribucion al desempeño

#mostrar un dataframe con metricas (los primeros 10 renglones)

#main.py
#---------------------------------------------------------------------------------------------------------- Paso 1.10
# -- plot de comparacion entre estrategias


