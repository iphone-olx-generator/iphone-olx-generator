from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI()  # klucz bierze z ENV OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')  # tutaj masz swoją stronę startową

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    # Tworzymy prompt na podstawie danych z JSONa
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

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś sprzedawcą telefonów, piszesz profesjonalne i zachęcające opisy."},
                {"role": "user", "content": prompt}
            ]
        )
        description = response.choices[0].message.content
        return jsonify({"description": description})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
