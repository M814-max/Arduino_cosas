from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def obtener_informacion_arduino(termino):
    url = "https://www.arduino.cc/reference/en/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Buscar enlaces que coincidan con el término
    resultados = soup.find_all("a", string=lambda text: text and termino.lower() in text.lower())
    
    if resultados:
        # Extraer y limpiar la URL
        href = resultados[0].get('href')
        if href.startswith('http'):
            return href
        else:
            return "https://www.arduino.cc" + href
    else:
        return "No se encontró información sobre el término."

@app.route('/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('termino')
    resultado = obtener_informacion_arduino(termino)
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
