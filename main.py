from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Klucz API z ENV (albo wpisz tu, ale lepiej z ENV)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return "Twoja usługa działa 🚀"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Brak prompta"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Lepiej na start gpt-3.5-turbo niż GPT-4
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
