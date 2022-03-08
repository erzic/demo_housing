from utilities import limpiar_precios,limpiar_m2, limpiar_location
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

df_master = pd.DataFrame()
c=0

while True:
    titulos = []
    precio = []
    location = []
    tamano = []
    
    if c==0:
        url_encuentra24 = "https://www.encuentra24.com/el-salvador-es/bienes-raices-venta-de-propiedades-casas"
    else:
        url_short = "https://www.encuentra24.com"
        new_page = s.find("a", attrs={"title":"Continuar"}).get("href")
        url_encuentra24 = "".join([url_short,new_page])

    print(url_encuentra24)
    df_temp = pd.DataFrame()
    response = requests.get(url_encuentra24)

    s = BeautifulSoup(response.text, "lxml")

    articulos_casa = s.findAll("article", attrs={"itemprop": "itemListElement"})
    next_page = s.find("a", attrs={"rel":"next"}).get("href")

    for articulo in articulos_casa:
        titulos.append(articulo.find("div", attrs={"itemprop":"name"}).text)
        precio.append(articulo.find("div", attrs={"itemprop":"price"}).text)
        location.append(articulo.find("span", attrs={"class":"ann-info-item"}).text)
        tamano.append(articulo.find("span", attrs={"class":"value"}).text)


    url_short = "https://www.encuentra24.com"
    new_page = s.find("a", attrs={"title":"Continuar"}).get("href")
    url_encuentra24 = "".join([url_short,new_page])

    df_temp = pd.DataFrame({"titulos":titulos, "precios":precio, "location":location,"tamano":tamano})

    df_master = pd.concat([df_master, df_temp])

    c+=1