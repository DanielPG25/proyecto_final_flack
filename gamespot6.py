import requests
import os
import sys

url_base= "https://www.gamespot.com/api/"
key=os.environ["KEY"]
parametros={"api_key":key,"format":"json","field_list":"categories"}
cabeceras={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
if r.status_code==200:
	doc = r.json()
	lista = []
	for categoria in doc.get('results'):
		for cat in categoria.get('categories'):
			if cat.get('name') not in lista:
				lista.append(cat.get('name'))
	for a in lista:
		print(a)