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

@app.route("/herramientas", methods=["GET", "POST"])
def herramientas():
    return render_template("herramientas.html")

@app.route("/calculadora_peso_ideal", methods=["GET", "POST"])
def calculadora_peso_ideal():
    resultado = None

    if request.method == "POST":
        try:
            altura = float(request.form.get("altura"))
            sexo = request.form.get("sexo")

            altura_m = altura / 100

            if sexo == "hombre":
                peso_ideal = 50 + 2.3 * ((altura_m * 100 / 2.54) - 60)
            else:
                peso_ideal = 45.5 + 2.3 * ((altura_m * 100 / 2.54) - 60)

            resultado = round(peso_ideal, 2)

        except:
            resultado = "Error: Verifica los datos ingresados."

    return render_template("herramientas.html", resultado=resultado)

@app.route("/calculadora_macros", methods=["GET", "POST"])
def calculadora_macros():
    resultados = None

    if request.method == "POST":
        try:
            calorias = float(request.form.get("calorias"))
            objetivo = request.form.get("objetivo")
            
            if objetivo == "perdida":
                pct_prot, pct_grasas, pct_carbs = 0.30, 0.25, 0.45

            elif objetivo == "mantenimiento":
                pct_prot, pct_grasas, pct_carbs = 0.25, 0.30, 0.45

            elif objetivo == "ganancia":
                pct_prot, pct_grasas, pct_carbs = 0.30, 0.25, 0.45

            proteinas = round((calorias * pct_prot) / 4, 1)
            grasas = round((calorias * pct_grasas) / 9, 1)
            carbohidratos = round((calorias * pct_carbs) / 4, 1)

            resultados = {
                "proteinas": proteinas,
                "grasas": grasas,
                "carbohidratos": carbohidratos,
            }

        except:
            resultados = "Error: Verifica tus datos."

    return render_template("herramientas.html", macros=resultados)



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