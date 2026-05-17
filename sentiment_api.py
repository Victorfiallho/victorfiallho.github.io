from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
CORS(app)

# Treinar o modelo
data = {
    'texto': [
        'Eu amo este modelo de IA', 'Isso é maravilhoso', 'Que algoritmo incrível',
        'Eu odeio erros de sintaxe', 'Este resultado está péssimo', 'Muito ruim e lento'
    ],
    'sentimento': [1, 1, 1, 0, 0, 0]
}

df = pd.DataFrame(data)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['texto'])
modelo = LogisticRegression()
modelo.fit(X, df['sentimento'])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    texto = data.get('texto', '')

    if not texto:
        return jsonify({'erro': 'Texto vazio'}), 400

    frase_vetorizada = vectorizer.transform([texto])
    predicao = modelo.predict(frase_vetorizada)[0]
    confianca = modelo.predict_proba(frase_vetorizada)[0]

    resultado = {
        'texto': texto,
        'sentimento': 'Positivo' if predicao == 1 else 'Negativo',
        'confianca': float(max(confianca) * 100)
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
