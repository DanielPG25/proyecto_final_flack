import requests
import os
import sys

url_base= "https://www.gamespot.com/api/"
key=os.environ["KEY"]
nombre="title:" + input("Dime el nombre del artículo: ")
parametros={"api_key":key,"format":"json","filter":nombre,"offset":0}
cabeceras={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
print(r.url)
if r.status_code==200:
	doc = r.json()
	for articulos in doc.get('results'):
		print(articulos.get('title'),' ',articulos.get('id'))