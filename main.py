from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = f"""
    Napisz atrakcyjny opis do ogłoszenia OLX na podstawie poniższych danych:
    - Model: {data.get('model', '')}
    - Stan: {data.get('condition', '')}
    - Pamięć: {data.get('storage', '')}
    - Kolor: {data.get('color', '')}
    - Bateria: {data.get('battery', '')}
    - Dodatki: {data.get('extras', '')}
    - Uwagi: {data.get('notes', '')}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś sprzedawcą telefonów, piszesz profesjonalne i zachęcające opisy."},
            {"role": "user", "content": prompt}
        ]
    )
    description = response.choices[0].message.content
    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
