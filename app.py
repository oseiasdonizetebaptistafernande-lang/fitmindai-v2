from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
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
    dias = request.form.get("dias")

    prompt = f"""
    Crie um plano de treino completo e organizado.

    Objetivo: {objetivo}
    Peso: {peso}
    Altura: {altura}
    Nível: {nivel}
    Dias disponíveis: {dias}

    Quero:
    - divisão dos treinos
    - exercícios
    - séries
    - repetições
    - cardio
    - alimentação
    """

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

    return render_template(
        "resultado.html",
        treino=treino,
        objetivo=objetivo,
        peso=peso,
        altura=altura,
        nivel=nivel,
        dias=dias
    )

if __name__ == "__main__":
    app.run(debug=True)
