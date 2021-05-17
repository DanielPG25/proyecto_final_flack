import requests
import os
import sys

url_base= "https://www.gamespot.com/api/"
key=os.environ["KEY"]
id_="id:"+input("Dime la id del articulo: ")
direcc = id_+":asc"
parametros={"api_key":key,"format":"json","filter":id_,"limit":1,"sort":direcc}
cabeceras={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
if r.status_code==200:
	doc = r.json()
	for juegos in doc.get('results'):
		print(juegos.get('publish_date'))
		print(juegos.get('title'))
		print(juegos.get('authors'))
		print(juegos.get('deck'))
		print(juegos.get('body'))
		print(juegos.get('lede'))
		for a in juegos.get('categories'):
			print(a.get('name'))
		print(juegos.get('site_detail_url'))