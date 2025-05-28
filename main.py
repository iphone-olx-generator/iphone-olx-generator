from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = f"""
    Napisz atrakcyjny opis do ogłoszenia OLX na podstawie poniższych danych:
    - Model: {data['model']}
    - Stan: {data['condition']}
    - Pamięć: {data['storage']}
    - Kolor: {data['color']}
    - Bateria: {data['battery']}
    - Dodatki: {data['extras']}
    - Uwagi: {data['notes']}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś sprzedawcą telefonów, piszesz profesjonalne i zachęcające opisy."},
            {"role": "user", "content": prompt}
        ]
    )

    description = response['choices'][0]['message']['content']
    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
