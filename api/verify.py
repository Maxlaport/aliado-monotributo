from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# --- INICIO DE CÓDIGO DE DIAGNÓSTICO ---
print("INICIANDO SCRIPT: api/verify.py")
# Obtenemos la ruta del directorio donde se está ejecutando este script
current_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Directorio actual detectado: {current_dir}")

# Listamos todos los archivos en ese directorio para ver si los padrones están ahí
try:
    files_in_dir = os.listdir(current_dir)
    print(f"Archivos encontrados en el directorio: {files_in_dir}")
except Exception as e:
    print(f"Error al listar archivos del directorio: {e}")
# --- FIN DE CÓDIGO DE DIAGNÓSTICO ---


def verify_cuit(cuit, jur):
    padron_files = {
        "AGIP": "padron_agip.txt",
        "ARBA": "padron_arba.txt"
    }
    
    filename = padron_files.get(jur)
    if not filename:
        return {"error": f"Jurisdicción '{jur}' no es válida."}

    # Usamos la ruta detectada al inicio para construir la ruta completa al archivo
    file_path = os.path.join(current_dir, filename)
    print(f"Intentando abrir el archivo en la ruta: {file_path}")

    if not os.path.exists(file_path):
        print(f"ERROR CRÍTICO: El archivo no existe en la ruta '{file_path}'")
        return {"error": f"Archivo de padrón '{filename}' no encontrado en el servidor."}

    try:
        df = pd.read_csv(file_path, sep=';', header=None, dtype=str)
        df.columns = ['CUIT', 'Alicuota']
        
        result = df[df['CUIT'] == cuit]
        
        if not result.empty:
            alicuota = result['Alicuota'].iloc[0]
            return {
                "encontrado": True,
                "cuit_consultado": cuit,
                "jurisdiccion": f"{jur}",
                "resultado": {
                    "tipo_alicuota": "Retención/Percepción",
                    "alicuota": f"{alicuota}%",
                    "mensaje": f"Se debe aplicar una alícuota del {alicuota}%."
                },
                "fuente_de_datos": {
                    "nombre_padron": f"Padrón de Ejemplo - Junio 2025 ({jur})",
                }
            }
        else:
             return {
                "encontrado": False,
                "cuit_consultado": cuit,
                "jurisdiccion": f"{jur}",
                "mensaje": "El CUIT no se encuentra en el padrón."
            }
    except Exception as e:
        print(f"ERROR CRÍTICO DURANTE LECTURA DE PADRÓN: {str(e)}")
        return {"error": f"Error procesando el padrón: {str(e)}"}

@app.route('/api/verify', methods=['GET'])
def handle_verify():
    print("Recibida una petición a /api/verify")
    cuit = request.args.get('cuit')
    jur = request.args.get('jur')

    if not cuit or not jur:
        return jsonify({"error": "CUIT y Jurisdicción son requeridos."}), 400
    
    response_data = verify_cuit(cuit, jur)
    return jsonify(response_data)
