from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# ========================
# FUNCIONES DE USUARIOS
# ========================
def cargar_usuarios():
    with open("usuarios.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# ========================
# FUNCIONES DE MOVIES
# ========================
def cargarMovies():
    with open('data/biblioteca.json', 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardarMovies(data):
    with open("data/biblioteca.json", "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, ensure_ascii=False, indent=4)

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

def filtrar_por_categoria(lista, categoria):
    if not categoria:
        return lista

    lista_filtrada = []
    for item in lista:
        if 'categorias' in item:
            if categoria in item['categorias']:
                lista_filtrada.append(item)
    return lista_filtrada

def obtener_nuevo_id():
    data = cargarMovies()
    if not data:
        return 1
    max_id = max(item["id"] for item in data)
    return max_id + 1

# ========================
# RUTAS PRINCIPALES
# ========================
@app.route("/")
def index():
    data = cargarMovies()
    categoria_filtrada = request.args.get('categoria')
    data = filtrar_por_categoria(data, categoria_filtrada)
    return render_template("index.html", data=data)

@app.route("/peliculas")
def peliculas():
    peliculas, _ = dividir()
    categoria_filtrada = request.args.get('categoria')
    peliculas = filtrar_por_categoria(peliculas, categoria_filtrada)
    return render_template("peliculas.html", peliculas=peliculas)

@app.route("/series")
def series():
    _, series = dividir()
    categoria_filtrada = request.args.get('categoria')
    series = filtrar_por_categoria(series, categoria_filtrada)
    return render_template("series.html", series=series)

# ========================
# LOGIN y LOGOUT
# ========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        usuarios = cargar_usuarios()

        for user in usuarios:
            if user["usuario"] == usuario and user["contrasena"] == contrasena:
                session["usuario"] = usuario
                session["rol"] = user["rol"]
                flash("Sesión iniciada con éxito", "success")
                return redirect(url_for("index"))

        flash("Usuario o contraseña incorrectos", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("index"))

# ========================
# AGREGAR (solo admin)
# ========================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if 'usuario' not in session or session.get('rol') != 'admin':
        flash("Acceso denegado. Solo administradores pueden ingresar aquí.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        nueva_entrada = {
            "id": obtener_nuevo_id(),
            "titulo": request.form["titulo"],
            "descripcion": request.form["descripcion"],
            "imagen": request.form["imagen"],
            "categoria": request.form["categoria"],
            "tipo": request.form["tipo"]
        }

        data = cargarMovies()
        data.append(nueva_entrada)
        guardarMovies(data)
        flash("Contenido agregado correctamente", "success")
        return redirect("/")

    return render_template("agregar.html")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    app.run(debug=True)
