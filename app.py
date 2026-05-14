from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():

    objetivo = request.form.get("objetivo")
    peso = request.form.get("peso")
    altura = request.form.get("altura")
    nivel = request.form.get("nivel")

    segunda = request.form.get("segunda")
    terca = request.form.get("terca")
    quarta = request.form.get("quarta")
    quinta = request.form.get("quinta")
    sexta = request.form.get("sexta")

    prompt = f"""
Você é um personal trainer profissional.

Crie um plano de treino COMPLETAMENTE EM HTML.

NÃO use markdown.
NÃO use texto puro.

Crie um visual organizado.

Use:

<div>
<h2>
<h3>
<table>
<tr>
<td>
<ul>
<li>

Organize:

- informações do cliente
- divisão dos treinos
- exercícios
- séries
- repetições
- descanso
- cardio
- alimentação

Cada treino deve ficar separado.

Crie tabelas para exercícios.

Cliente:

Objetivo: {objetivo}
Peso: {peso}
Altura: {altura}
Nível: {nivel}

Treinos:

Segunda: {segunda}
Terça: {terca}
Quarta: {quarta}
Quinta: {quinta}
Sexta: {sexta}

"""

    resposta = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    resultado = resposta.choices[0].message.content

    return render_template(
        "index.html",
        resposta=resultado
    )

if __name__ == "__main__":
    app.run(debug=True)
