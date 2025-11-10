from flask import Flask, render_template , request, redirect, url_for, flash, session
from datetime import datetime 

app = Flask(__name__)
app.secret_key = "Nutriflow1234"

usuarios = [
    {
        "nombre": "Nombre",
        "email": "usuario@gmail.com",
        "contraseña": "1234"
    }
]

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


        if email == "usuario@gmail.com" and password == "1234":
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
        session["nombre"] = request.form.get("nombre")
        session["apellidos"] = request.form.get("apellidos")
        session["edad"] = request.form.get("edad")
        session["sexo"] = request.form.get("sexo")
        session["actividad"] = request.form.get("actividad")
        session["peso"] = request.form.get("peso")
        session["altura"] = request.form.get("altura")
        session["email"] = request.form.get("email")
        session["password"] = request.form.get("password")
        session["objetivos"] = request.form.get("objetivos")
        session["alergias"] = request.form.get("alergias")
        session["intolerancias"] = request.form.get("intolerancias")
        session["dietas"] = request.form.get("dietas")
        session["no_gusta"] = request.form.get("no_gusta")

        session["usuario"] = session["nombre"]
        flash(f"¡Bienvenido, {session['nombre']}! Registro exitoso.", "success")
        return redirect(url_for("index"))

    return render_template("registrarse.html")
if __name__ == "__main__":
    app.run(debug=True)