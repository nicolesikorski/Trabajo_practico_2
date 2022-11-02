
""" >>>> NO TOCAR ESTE CÓDIGO >>>> """

from operator import index
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def str2datetime(date, fmt="%Y-%m-%d"):
    """Convierte una cadena (o secuencia de cadenas) a tipo datetime (o secuencia de datetimes).

    ENTRADAS:
        date (str ó secuencia de str): fechas a convertir.
        fmt (str, opcional): formato de fecha (ver documentación de biblioteca datetime).
    SALIDAS:
        output (datetime ó secuencia de datetime): fechas convertidas a datetime.
    EJEMPLOS:
    >>>> date = str2datetime('2022-10-24')
    >>>> print(date.year, date.month, date.day)

    >>>> date = str2datetime(['2022-10-24', '2022-10-23', '2022-10-22'])
    >>>> print(len(date))"""
    if isinstance(date, str):
        return datetime.strptime(date, fmt)
    elif isinstance(date, (list, np.ndarray)):
        output = []
        for d in date:
            output.append(datetime.strptime(d, fmt))
        if isinstance(date, np.ndarray):
            output = np.array(output)
        return output


def datetime2str(date, fmt="%Y-%m-%d"):
    """Convierte un datetime (o secuencia de datetimes) a tipo str (o secuencia de str).

    ENTRADAS:
        date (datetime ó secuencia de datetime): fechas a convertir.
        fmt (str, opcional): formato de fecha (ver documentación de biblioteca datetime).
    SALIDAS:
        output (str ó secuencia de str): fechas convertidas a cadenas.
    EJEMPLOS:
    >>>> date_str = '2022-10-24'
    >>>> date = str2datetime(date_str)
    >>>> print(datetime2str(date) == date_str)"""
    if isinstance(date, datetime):
        return date.strftime(fmt)
    elif isinstance(date, (list, np.ndarray)):
        output = []
        for d in date:
            output.append(d.strftime(fmt))
        if isinstance(date, np.ndarray):
            output = np.array(output)
        return output


""" >>>> DEFINAN SUS FUNCIONES A PARTIR DE AQUÍ >>>> """

#Analisis de datos
#1


def readfile (archivo):
    dict= { }
    with open (archivo, 'r') as file:
        for i, linea in enumerate(file, 1):
            linea= linea.rstrip('\n')
            if i == 1:
                nombre_columnas= linea.split(',')
                for nombre in nombre_columnas:
                    dict[nombre.strip()]= []
            else:
                datos_linea= linea.split(',')
                for i, datos in enumerate (datos_linea):
                    if i == 0:
                        date= str2datetime(datos)
                        dict[nombre_columnas[i].strip()].append(date)
                    else:
                        dict[nombre_columnas[i].strip()].append(float(datos))
                    
    return dict

diccionario = readfile('bolsa.csv') #En diccionario está el diccionario


#2 (Funcion monthly_average)

def monthly_average(accion, diccionario): 
    #Sacar precio promedio de todos los meses
    #Fijarme como indicarle al programa que termino el mes: 
    lista_provisoria = []
    meses = []
    promedios = []
    fecha_primer_dia = []

    fechas = diccionario["Date"]
    i = 0
    while i < len(fechas):
        if i+1 != len(fechas):
            if fechas[i].month != fechas[i+1].month:
                lista_provisoria.append(diccionario[accion][i])
                meses.append(lista_provisoria)
                lista_provisoria = []
            else:
                lista_provisoria.append(diccionario[accion][i])
        else:
            meses.append(lista_provisoria)
        i += 1
    for x in meses:
        promedios.append((sum(x)/len(x)))

    lista_provisoria1 = []
    contador = 0
    while contador < len(fechas):
        if contador+1 != len(fechas):
            if fechas[contador].month != fechas[contador+1].month:
                lista_provisoria1.append(fechas[contador])
                fecha_primer_dia.append(lista_provisoria1[0])
                lista_provisoria1 = []
            else:
                lista_provisoria1.append(diccionario["Date"][contador])
        else:
            fecha_primer_dia.append(lista_provisoria1[0])
        contador += 1
    return fecha_primer_dia, promedios

fecha_primer, promedio = monthly_average('SATL', diccionario)


#3
with open('monthly_average_SATL.csv','w') as archivo:
    for i,fecha in enumerate(fecha_primer):
        linea = f'{fecha_primer[i]}, {str(promedio[i])}\n'
        archivo.write(linea)

    #tiene que devolver
    # fechas: ['2021-01-01', ' 2021-02-01', ..., '2021-12-01']
    # promedios: [89.99, 67.36, ..., 78.76]
    # tengo que ir fecha por fecha sumando cada precio en una lista cuando cambia de mes, calculo el promedio de la lista que tenia 
    # guardo el promedio 
    # vacio la lista
    # arranco devuelta
    
    # cuando cambia el mes? --> cuando el del medio es distitno al que venia siendo


#4
def max_gain(nombre_accion,diccionario,fecha_venta):
    lista_de_precios = np.array(diccionario[nombre_accion][0:diccionario["Date"].index(fecha_venta)])
    precio_inversion = lista_de_precios.min()
    fecha_de_inversion = diccionario["Date"][lista_de_precios.argmin()]
    precio_de_venta = diccionario[nombre_accion][diccionario["Date"].index(fecha_venta)]
    ganancia = (precio_de_venta-precio_inversion)/precio_inversion

    return fecha_de_inversion, ganancia
    

""" >>>> ESCRIBAN SU CÓDIGO A PARTIR DE AQUÍ >>>> """
fecha_mayor_ganancia, retorno_inversion = max_gain('SATL',diccionario,str2datetime("2022-06-06"))
print(fecha_mayor_ganancia, retorno_inversion)

#5

def report_max_gains(diccionario,fecha_venta):

    with open('resumen_mejor_compra.txt','w') as archivo:
        contador = 1
        while contador<len(diccionario.keys()):
            fecha, ganancias = max_gain(list(diccionario.keys())[contador], diccionario, fecha_venta)
            if ganancias > 0:
                archivo.write(f"{list(diccionario.keys())[contador]} genera una ganancia de {ganancias*100}% habiendo comprando en {fecha} y vendiendose en {fecha_venta}\n")
            else:
                archivo.write(f"{list(diccionario.keys())[contador]} genera una ganancia de {ganancias*100}% habiendo comprando en {fecha} y vendiendose en {fecha_venta}, La acción {list(diccionario.keys())[contador]} solo genera péridas\n")

            contador += 1
    

report_max_gains(diccionario,str2datetime("2022-06-06"))
