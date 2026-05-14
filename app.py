from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests
import markdown

app = Flask(__name__)
app.secret_key = "fitmindai"

# =========================
# CHAVE DA GROQ
# =========================

API_KEY = ""

# =========================
# CRIAR BANCO
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

        usuario = request.form["usuario"]
        senha = request.form["senha"]

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

        usuario = request.form["usuario"]
        senha = request.form["senha"]

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

@app.route("/home", methods=["GET", "POST"])
def home():

    if "usuario" not in session:
        return redirect("/")

    resultado = ""

    if request.method == "POST":

        objetivo = request.form["objetivo"]
        peso = request.form["peso"]
        dias = request.form["dias"]
        intensidade = request.form["intensidade"]

        treino_segunda = request.form["segunda"]
        treino_terca = request.form["terca"]
        treino_quarta = request.form["quarta"]
        treino_quinta = request.form["quinta"]
        treino_sexta = request.form["sexta"]

        prompt = f"""
Crie um treino EXTREMAMENTE ORGANIZADO.

Objetivo: {objetivo}
Peso: {peso}
Dias: {dias}
Intensidade: {intensidade}

SEGUNDA:
{treino_segunda}

TERÇA:
{treino_terca}

QUARTA:
{treino_quarta}

QUINTA:
{treino_quinta}

SEXTA:
{treino_sexta}

Organize assim:

# DIVISÃO SEMANAL

## Segunda-feira
- exercícios
- séries
- repetições
- descanso

## Terça-feira

## Quarta-feira

## Quinta-feira

## Sexta-feira

# CARDIO

# ALIMENTAÇÃO

## Alimentos recomendados para cada treino

## Café da manhã

## Pré treino

## Pós treino

## Jantar

## Alimentos proibidos

## Alimentos liberados às vezes

# DICAS IMPORTANTES

Deixe bonito e organizado.
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:

            resposta = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            resposta_json = resposta.json()

            texto = resposta_json["choices"][0]["message"]["content"]

            resultado = markdown.markdown(texto)

        except Exception as erro:

            resultado = f"""
            <div class='erro'>
                <h2>Erro da API</h2>
                <p>{erro}</p>
            </div>
            """

    return render_template(
        "index.html",
        resultado=resultado,
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
