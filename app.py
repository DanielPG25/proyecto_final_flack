from flask import Flask, render_template,request,abort
import requests
import json
import sys
import os
app = Flask(__name__)

url_base= "https://www.gamespot.com/api/"
key=os.environ["KEY"]
cabeceras={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}

@app.route('/',methods=["GET"])
def inicio():
	return render_template("inicio.html")

@app.route('/juegos',methods=["GET","POST"])
def juegos():
	if request.method=="GET":
		parametros={"api_key":key,"format":"json","field_list":"genres"}
		r=requests.get(url_base+"games/",params=parametros,headers=cabeceras)
		if r.status_code==200:
			doc = r.json()
			cat = []
			for genero in doc.get('results'):
				for genr in genero.get('genres'):
					if genr.get('name') not in cat:
						cat.append(genr.get('name'))			
			return render_template("juegos.html",datos=cat)
		else:
			abort(404)
	else:
		nombre="name:" + str(request.form.get("cad"))
		categoria = str(request.form.get("categoria_seleccionada"))
		parametros={"api_key":key,"format":"json","filter":nombre}
		r=requests.get(url_base+"games/",params=parametros,headers=cabeceras)
		if r.status_code==200:
			doc = r.json()
			datos = []
			error = True
			for juegos in doc.get('results'):
				for b in juegos.get('genres'):
					if categoria in b.get('name'):
						dicc={}
						dicc['nombre']=juegos.get('name')
						dicc['id']=juegos.get('id')
						datos.append(dicc)
						error = False
			return render_template("listajuegos.html",datos=datos,error=error,cad=categoria)
		else:
			abort(404)







port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)