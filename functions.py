
"""
# -- ---------------------------------------------------------------------------------------------------  -- #
# -- project:  Generar una estrategia de inversion para un capital de 1,000,000 de pesos                                                      -- #
# -- script: functions.py : se generan funciones del codigo para llamarlas cuando sean necesarias de utilizar                                       -- #
# -- author: elvis7bello                                                                                  -- #
# -- license: GPL-3.0 License                                                                             -- #
# -- repository: https://github.com/elvi7bello/myst_lab1_EBA                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
#FUNCTIONS.PY: Procesamiento de funciones

import pandas as pd
import numpy as np
import time
import yfinance as yf
from data import archivos, data_archivos, t_fechas, ic_fechas

#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.1
# -- Construir el vector de fechas a partir del vector de nombre de archivos
def f_fechas(archivos):
    """
    Descripcion:
    En esta funcion encontraremos los vectores que se necesitan para las fechas de acuerdo con el vector que se tiene
    en los archivos

    Parametros:
    archivos (list) es una lista con los nombres de los archivos a leer

    Returns:
    fechas (dict) es un diccionario con fechas en dos diferentes formatos
    {'i_fechas' = i_fechas, t_fechas' = t_fechas}

    """
    #etiquetas para dataframe y para yfinance
    t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    # lista con fechas ordenadas (para usarse como indexadores de archivos)
    i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

def f_tickers(archivos, data_archivos):
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

def f_obtener_precios(p_tickers, p_fechas):...

def f_pos_i(p_data_archivos, p_archivo_ini, p_precios, p_params):...

def f_pasiva(p_fechas, p_archivos, p_precios, p_pos_ini, p_params):...

#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.2
# -- Construir el vector de tickers utilizables en yahoo finance


#functions.py
#---------------------------------------------------------------------------------------------------------- Paso 1.3
# -- Descargar y acomodar todos los precios historicos



