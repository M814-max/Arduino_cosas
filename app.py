from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para hacer scraping de Arduino Reference
def obtener_informacion_arduino(termino):
    url = "https://www.arduino.cc/reference/en/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    resultados = soup.find_all("a", string=lambda text: text and termino.lower() in text.lower())
    if resultados:
        return "https://www.arduino.cc" + resultados[0].get('href')[2:]
    else:
        return "No se encontró información sobre el término."

# Endpoint para la búsqueda
@app.route('/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('termino')  # Captura el término de la URL (ej. ?termino=digitalWrite)
    resultado = obtener_informacion_arduino(termino)
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
