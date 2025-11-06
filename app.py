from flask import Flask, render_template , request, redirect, url_for, flash, session
from datetime import datetime 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/base")
def menu():
    return render_template("base.html") 

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/educacion")
def educacion():
    return render_template("educacion.html")

@app.route("/recetas")
def recetas():
    return render_template("recetas.html")

@app.route("/herramientas")
def herramientas():
    return render_template("herramientas.html")

@app.route("/iniciarS")
def login():
    return render_template("iniciarS.html")

@app.route("/registrarse")
def register():
    return render_template("registrarse.html")
if __name__ == "__main__":

    app.run(debug=True)