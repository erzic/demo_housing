from utilities import limpiar_precios,limpiar_m2, limpiar_location
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
#from requests_html import HTMLSession

from selenium import webdriver

df_master = pd.DataFrame()
c=0

def limpieza_campos(header):
    columnas = [i.text for i in header.findAll("span", attrs={"class":"info-name"})]
    valores = [i.text for i in header.findAll("span", attrs={"class":"info-value"})]

    return pd.DataFrame({i:[v] for (i,v) in zip(columnas, valores)})



while True:
    titulos = []
    precio = []
    location = []
    tamano = []
    
    if c==0:
        url_encuentra24 = "https://www.encuentra24.com/el-salvador-es/bienes-raices-venta-de-propiedades-casas"
        url_short = "https://www.encuentra24.com"
    else:
        url_short = "https://www.encuentra24.com"
        new_page = s.find("a", attrs={"title":"Continuar"}).get("href")
        url_encuentra24 = "".join([url_short,new_page])

    response = requests.get(url_encuentra24)

    s = BeautifulSoup(response.text, "lxml")

    articulos_casa = s.findAll("article", attrs={"itemprop": "itemListElement"})
    try:
        next_page = s.find("a", attrs={"rel":"next"}).get("href")
    except:
        break
    
    print(f"link pagina {url_encuentra24}")

    # sacamos cada casa en cada page

    link_casas = s.findAll('a', attrs={'class':'ann-box-title', 'itemprop':'url'})

    # recorremos cada casa en cada page
    
    for link in link_casas:
        df_pagina_1 = pd.DataFrame()
        df_pagina_2 = pd.DataFrame()
        info_casa = requests.get(''.join([url_short,link.get("href")]))
        #print(''.join([url_short,link.get("href")]))
        s_casa = BeautifulSoup(info_casa.text, 'lxml')

        header_casa_1 = s_casa.find('div', attrs={'class':'ad-info'})
        try:
            df_header_casa_1 = limpieza_campos(header_casa_1)
        except:
            continue

        header_casa_2 = s_casa.find('div', attrs={'class':'ad-details'})
        df_header_casa_2 = limpieza_campos(header_casa_2)
        beneficios = s_casa.find('div', attrs={'class':'section-box'})
    
        scripts = s_casa.findAll("script", attrs={"type":"text/javascript"})
        try:
            script_con_location = [script for script in scripts if script.text.find("https://www.google.com/maps/embed") != -1][0].text

            lat_long = script_con_location.split("&q=")[1].split("&zoom=")[0]
        except:
            #print("No existe data geogr??fica")
            lat_long = np.nan
            pass

        df_temp_2 = pd.concat([df_header_casa_1, df_header_casa_2], axis=1)
        df_temp_2["link"] = ''.join([url_short,link.get("href")])
        df_temp_2["beneficios_var"] = beneficios.text

        try:
            df_temp_2["lat_long"] = lat_long
        except:
            df_temp_2["lat_long"] = np.nan
        
        df_master = pd.concat([df_master, df_temp_2],ignore_index=True)

    c+=1
    #df_master.reset_index(inplace=True)


df_master_limpio =  df_master.copy()

df_master_limpio["Precio:"]= df_master_limpio["Precio:"].apply(limpiar_precios)
df_master_limpio["Precio/M?? de construcci??n:"] = df_master_limpio["Precio/M?? de construcci??n:"].apply(limpiar_precios)


# limpiando dataframe
cols = [i.replace(":", "").replace("/M??", "/m2") for i in df_master_limpio.columns()]

df_master_limpio = pd.DataFrame(df_master_limpio.values, columns=cols)

df_master_limpio.to_csv("encuentra24_ventas_casas.csv", encoding="utf-8")