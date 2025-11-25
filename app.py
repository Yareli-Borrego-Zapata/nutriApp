from flask import Flask, render_template , request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, cheeck_pasword_hash
from datetime import datetime 

app = Flask(__name__)
app.secret_key = "Nutriflow1234"
#esta es la configuracion del mysql

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'NutriFlow'

#aver horita le movemos

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


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

#1 imc
@app.route("/calculadora_imc", methods=["GET", "POST"])
def calculadora_imc():
    imc = None
    categoria = None
    mensaje = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura")) / 100

            imc = round(peso / (altura ** 2), 2)

            if imc < 18.5:
                categoria = "Bajo peso"
                mensaje = "Tu IMC indica bajo peso. Asegúrate de recibir suficientes nutrientes."

            elif 18.5 <= imc < 24.9:
                categoria = "Normal"
                mensaje = "¡Excelente! Tu IMC está dentro de lo saludable. Mantén tus buenos hábitos."

            elif 25 <= imc < 29.9:
                categoria = "Sobrepeso"
                mensaje = "Tu IMC indica sobrepeso. Ajustes en alimentación y actividad física pueden ayudarte."

            else:
                categoria = "Obesidad"
                mensaje = "Tu IMC está en rango de obesidad. Te recomendamos consultar a un profesional de salud."

        except:
            imc = "Error"
            categoria = "Datos inválidos."
            mensaje = "Verifica que los valores ingresados sean correctos."

    return render_template("herramientas.html", imc=imc, categoria=categoria, mensaje=mensaje)

#2 tmb
@app.route("/calculadora_tmb", methods=["GET", "POST"])
def calculadora_tmb():
    tmb = None
    mensaje_tmb = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            edad = int(request.form.get("edad"))
            sexo = request.form.get("sexo")
            
            if sexo == "hombre":
                tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
            else:
                tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

            tmb = round(tmb, 2)
            mensaje_tmb = 'Este es el número aproximado de calorías que tu cuerpo necesita en reposo.'

        except:
            tmb = "Error: Verifica tus datos."

    return render_template("herramientas.html", tmb=tmb , mensaje_tmb=mensaje_tmb)

#3gct
@app.route("/calculadora_gct", methods=["GET", "POST"])
def calculadora_gct():
    gct = None
    mensaje_gct = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            edad = int(request.form.get("edad"))
            sexo = request.form.get("sexo")
            actividad = request.form.get("actividad")
            if sexo == "hombre":
                tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
            else:
                tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

            factores = {
                "sedentario": 1.2,
                "ligero": 1.375,
                "moderado": 1.55,
                "activo": 1.725,
                "muy_activo": 1.9
            }

            gct = round(tmb * factores[actividad], 2)

            mensaje_gct = 'Este número representa la energía total que gastas al día considerando tu actividad.'
        except:
            gct = "Error: Verifica tus datos."

    return render_template("herramientas.html", gct=gct , mensaje_gct=mensaje_gct)

#4 peso ideal
@app.route("/calculadora_peso_ideal", methods=["GET", "POST"])
def calculadora_peso_ideal():
    resultado = None

    if request.method == "POST":
        altura = float(request.form.get("altura"))
        sexo = request.form.get("sexo")

        if sexo == "hombre":
            resultado = round(50 + 0.91 * (altura - 152.4), 1)
        else:
            resultado = round(45.5 + 0.91 * (altura - 152.4), 1)

    return render_template("herramientas.html", resultado=resultado)

#5 macros
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