from flask import Flask, render_template, request, redirect, session
from groq import Groq
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "fitmindai"

# =========================
# API DA GROQ
# =========================

client = Groq(
    api_key=os.getenv("API_KEY")
)

# =========================
# BANCO DE DADOS
# =========================

def criar_banco():

    conn = sqlite3.connect("usuarios.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)

    conn.commit()
    conn.close()

criar_banco()

# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
            (usuario, senha)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["usuario"] = usuario

            return redirect("/home")

    return render_template("login.html")

# =========================
# CADASTRO
# =========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        conn = sqlite3.connect("usuarios.db")

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("cadastro.html")

# =========================
# HOME
# =========================

@app.route("/home")
def home():

    if "usuario" not in session:
        return redirect("/")

    return render_template(
        "index.html",
        usuario=session["usuario"]
    )

# =========================
# GERAR TREINO
# =========================

@app.route("/gerar", methods=["POST"])
def gerar():

    if "usuario" not in session:
        return redirect("/")

    objetivo = request.form.get("objetivo")
    peso = request.form.get("peso")
    altura = request.form.get("altura")
    intensidade = request.form.get("intensidade")

    segunda = request.form.get("segunda")
    terca = request.form.get("terca")
    quarta = request.form.get("quarta")
    quinta = request.form.get("quinta")
    sexta = request.form.get("sexta")

    prompt = f"""
Você é um personal trainer profissional.

Crie um treino EXTREMAMENTE ORGANIZADO.

Objetivo:
{objetivo}

Peso:
{peso}

Altura:
{altura}

Intensidade:
{intensidade}

DIVISÃO:

Segunda:
{segunda}

Terça:
{terca}

Quarta:
{quarta}

Quinta:
{quinta}

Sexta:
{sexta}

IMPORTANTE:

- treino organizado
- exercícios separados
- séries
- repetições
- descanso
- cardio
- alimentação
- alimentos recomendados
- alimentos proibidos
- motivação

Deixe tudo bonito.
"""

    try:

        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        treino = resposta.choices[0].message.content

    except Exception as erro:

        treino = f"""
Erro da IA:

{erro}
"""

    return render_template(
        "index.html",
        treino=treino,
        usuario=session["usuario"]
    )

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# =========================
# RODAR APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
