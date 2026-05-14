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

    treino = {
        "segunda": {
            "titulo": "Peito",
            "exercicios": [
                ["Supino Inclinado", "3", "12"],
                ["Supino Reto", "3", "12"],
                ["Crucifixo", "3", "12"]
            ]
        },

        "terca": {
            "titulo": "Costas",
            "exercicios": [
                ["Puxada Frontal", "3", "12"],
                ["Remada Curvada", "3", "12"],
                ["Pulldown", "3", "12"]
            ]
        },

        "quarta": {
            "titulo": "Pernas",
            "exercicios": [
                ["Agachamento", "4", "12"],
                ["Leg Press", "4", "10"],
                ["Mesa Flexora", "3", "12"]
            ]
        },

        "quinta": {
            "titulo": "Ombros",
            "exercicios": [
                ["Desenvolvimento", "3", "12"],
                ["Elevação Lateral", "3", "12"],
                ["Arnold Press", "3", "10"]
            ]
        },

        "sexta": {
            "titulo": "Braços",
            "exercicios": [
                ["Rosca Direta", "3", "12"],
                ["Tríceps Pulley", "3", "12"],
                ["Rosca Martelo", "3", "12"]
            ]
        }
    }

    return render_template(
        "index.html",
        objetivo=objetivo,
        peso=peso,
        altura=altura,
        nivel=nivel,
        treino=treino
    )

if __name__ == "__main__":
    app.run(debug=True)
