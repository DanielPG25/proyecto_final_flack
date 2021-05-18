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
def juegosl():
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
			return render_template("listajuegos.html",datos=datos,error=error,cad=request.form.get("cad"))
		else:
			abort(404)

@app.route('/juego/<identificador>')
def detallejuego(identificador):
	datos=[]
	ind = True
	id_="id:"+ identificador
	direcc = id_+":asc"
	parametros={"api_key":key,"format":"json","filter":id_,"limit":1,"sort":direcc}
	r=requests.get(url_base+"games/",params=parametros,headers=cabeceras)
	if r.status_code==200:
		doc = r.json()
		for juegos in doc.get('results'):
			ind = False
			dicc={}
			dicc['nombre']=juegos.get('name')
			dicc['descripcion']=juegos.get('description')
			dicc['fecha']=juegos.get('release_date')
			dicc['imagen']=juegos.get('image').get('original')
			dicc['tematica']=juegos.get('themes')
			dicc['franquicias']=juegos.get('franchises')
			dicc['url']=juegos.get('site_detail_url')
			dicc['generos']=juegos.get('genres')
			datos.append(dicc)
		if ind:
			abort(404)
		else:
			return render_template("detallesjuegos.html",datos=datos)
	else:
		abort(404)

@app.route('/noticias',methods=["GET","POST"])
def noticias():
	if request.method=="GET":
		parametros={"api_key":key,"format":"json","field_list":"categories"}
		r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
		if r.status_code==200:
			doc = r.json()
			lista = []
			for categoria in doc.get('results'):
				for cat in categoria.get('categories'):
					if cat.get('name') not in lista:
						lista.append(cat.get('name'))
			return render_template("noticias.html",datos=lista)
		else:
			abort(404)
	else:
		nombre="title:" + str(request.form.get("cad"))
		categoria = str(request.form.get("categoria_seleccionada"))
		parametros={"api_key":key,"format":"json","filter":nombre,"offset":0}
		r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
		if r.status_code==200:
			doc = r.json()
			datos = []
			error = True
			for articulos in doc.get('results'):
				for genr in articulos.get('categories'):
					if categoria in genr.get('name'):
						dicc={}
						dicc['nombre']=articulos.get('title')
						dicc['id']=articulos.get('id')
						datos.append(dicc)
						error=False
			return render_template("listanoticias.html",datos=datos,error=error,cad=request.form.get("cad"))
		else:
			abort(404)


@app.route('/noticia/<identificador>')
def detallenoticia(identificador):
	datos=[]
	ind = True
	id_="id:"+ identificador
	direcc = id_+":asc"
	parametros={"api_key":key,"format":"json","filter":id_,"limit":1,"sort":direcc}
	r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
	if r.status_code==200:
		doc = r.json()
		for articulo in doc.get('results'):
			ind = False
			dicc={}
			dicc['nombre']=articulo.get('title')
			dicc['autor']=articulo.get('authors')
			dicc['fecha']=articulo.get('publish_date')
			dicc['deck']=articulo.get('deck')
			dicc['body']=articulo.get('body')
			dicc['ledes']=articulo.get('lede')
			dicc['url']=articulo.get('site_detail_url')
			dicc['generos']=articulo.get('categories')
			datos.append(dicc)
		if ind:
			abort(404)
		else:
			return render_template("detallesnoticias.html",datos=datos)
	else:
		abort(404)

@app.route('/noticias/<categoria>')
def categoriasnoticia(categoria):
	nombre="genres:" + categoria
	parametros={"api_key":key,"format":"json","filter":nombre,"offset":0}
	r=requests.get(url_base+"articles/",params=parametros,headers=cabeceras)
	if r.status_code==200:
		doc = r.json()
		datos = []
		for articulos in doc.get('results'):
			dicc={}
			dicc['nombre']=articulos.get('title')
			dicc['id']=articulos.get('id')
			datos.append(dicc)
		return render_template("categoriasnoticias.html",datos=datos,cad=categoria)
	else:
		abort(404)

@app.route('/juegos/<categoria>')
def categoriasjuego(categoria):
	nombre="genres:" + categoria
	parametros={"api_key":key,"format":"json","filter":nombre,"offset":0}
	r=requests.get(url_base+"games/",params=parametros,headers=cabeceras)
	if r.status_code==200:
		doc = r.json()
		datos = []
		for articulos in doc.get('results'):
			dicc={}
			dicc['nombre']=articulos.get('name')
			dicc['id']=articulos.get('id')
			datos.append(dicc)
		return render_template("categoriasjuegos.html",datos=datos,cad=r.url)
	else:
		abort(404)












port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)