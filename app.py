from flask import Flask, render_template, request
import json

app = Flask(__name__)

def cargarMovies():
    with open('data/biblioteca.json', 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def dividir():
    data = cargarMovies()
    peliculas = []
    series = []
    for item in data:
        if item['tipo'] == 'Pelicula':
            peliculas.append(item)
        elif item['tipo'] == 'Serie':
            series.append(item)  
    return peliculas, series

@app.route("/")
def index():
    data = cargarMovies()
    categoria_filtrada = request.args.get('categoria')

    if categoria_filtrada:
        data_filtrada = []
        for item in data:
            if 'categorias' in item:
                if categoria_filtrada in item['categorias']:
                    data_filtrada.append(item)
        data = data_filtrada

    return render_template("index.html", data=data)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/peliculas")
def peliculas():
    datos = dividir()
    peliculas = datos[0]

    categoria_filtrada = request.args.get('categoria')

    if categoria_filtrada:
        peliculas_filtradas = []
        for pelicula in peliculas:
            if 'categorias' in pelicula:
                if categoria_filtrada in pelicula['categorias']:
                    peliculas_filtradas.append(pelicula)
        peliculas = peliculas_filtradas

    return render_template("peliculas.html", peliculas=peliculas)


@app.route("/series")
def series():
    datos = dividir()
    series = datos[1]

    categoria_filtrada = request.args.get('categoria')

    if categoria_filtrada:
        series_filtradas = []
        for serie in series:
            if 'categorias' in serie:
                if categoria_filtrada in serie['categorias']:
                    series_filtradas.append(serie)
        series = series_filtradas

    return render_template("series.html", series=series)


if __name__ == "__main__":
    app.run(debug=True)
