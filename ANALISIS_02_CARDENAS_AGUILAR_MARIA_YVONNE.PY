#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 16:57:05 2022

@author: Yvonne
"""
#%%

import pandas as pd

synergy = pd.read_csv('synergy_logistics_database.csv')

'''CREANDO UNA FUNCIÓN QUE PERMITA OBTENER LA FRECUENCIA Y EL VALOR TOTAL DE 
CUALQUIER AGRUPACIÓN '''

def grouping(df, groups):
    df['count'] = 1
    lista = df.groupby(groups).count()['count']
    lista = lista.to_frame()
    total_value = df.groupby(groups)['total_value'].sum()
    total_value = total_value.to_frame()
    lista['total_value'] = total_value['total_value']
    
    return lista

#%%

# PUNTO UNO

''' RUTAS DE IMPORTACIÓN Y EXPORTACIÓN - OBTENIENDO LAS RUTAS MÁS DEMANDADAS Y
ORDENÁNDOLAS POR FRECUENCIA Y POR VALOR TOTAL'''

demanded_routes = grouping(synergy, ['direction', 'origin', 'destination'])
demanded_routes = demanded_routes.sort_values(['count'], ascending = False)
demanded_routes.to_excel("demanded_routes.xlsx")
demanded_routes = demanded_routes.head(10)


recommended_routes = grouping(synergy, ['year', 'direction', 'origin', 'destination', 'transport_mode'])
recommended_routes = recommended_routes.sort_values(['total_value'], ascending = False)
recommended_routes.to_excel("recommended_routes.xlsx")
recommended_routes = recommended_routes.head(10)


#%%

# PUNTO DOS

''' MEDIOS DE TRANSPORTE - OBTENIENDO LOS MEDIOS DE TRANSPORTE MÁS IMPORTANTES '''

important_transport = grouping(synergy, ['transport_mode'])
important_transport = important_transport.sort_values(['total_value'], ascending = False)

#%%

# PUNTO TRES

''' MEDIOS DE TRANSPORTE - OBTENIENDO LAS RUTAS MÁS DEMANDADAS Y ORDENÁNDOLAS
POR FRECUENCIA Y POR VALOR TOTAL'''

total_total_value = synergy['total_value'].sum()

exports = synergy.loc[synergy['direction'] == 'Exports']
imports = synergy.loc[synergy['direction'] == 'Imports']

def countries(df, where):
    total_total_value = df['total_value'].sum()
    lista = df.groupby(where)['total_value'].sum()
    lista = lista.to_frame()
    lista['percentage %'] = lista['total_value']/total_total_value*100
    lista = lista.sort_values('percentage %', ascending = False)
    lista['accumulation'] = lista['percentage %'].cumsum()
    lista = lista[lista['accumulation'] < 80]
    
    return lista


countries_export_list = countries(exports, 'origin')

countries_import_list = countries(imports, 'destination')
    

