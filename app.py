from flask import Flask, render_template , request, redirect, url_for, flash, session
from datetime import datetime 

app = Flask(__name__)
app.secret_key = "Nutriflow123"

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

@app.route("/iniciarS", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        if email == "usuario@demo.com" and password == "1234":
            session["usuario"] = "Usuario Demo"
            flash("Inicio de sesión exitoso. ¡Bienvenido!", "success")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for("login"))
    return render_template("iniciarS.html")

@app.route("/cerrarS")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("index"))

@app.route("/registrarse", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        if not nombre or not email or not password:
            flash("Por favor, completa todos los campos obligatorios.", "warning")
            return redirect(url_for("register"))

        session["usuario"] = nombre
        flash(f"¡Bienvenido, {nombre}! Registro exitoso.", "success")
        return redirect(url_for("index"))

    return render_template("registrarse.html")
if __name__ == "__main__":

    app.run(debug=True)