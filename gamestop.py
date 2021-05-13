import requests
import os
import sys

url_base= "https://www.gamespot.com/api/"
key=os.environ["KEY"]
nombre="name:" + input("Dime el nombre del juego: ")
parametros={"api_key":key,"format":"json","filter":nombre}
cabeceras={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
r=requests.get(url_base+"games/",params=parametros,headers=cabeceras)
if r.status_code==200:
	doc = r.json()
	for juegos in doc.get('results'):
		print(juegos.get('name'))