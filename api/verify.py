from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
# Habilitamos CORS para permitir que el frontend se comunique con esta API
CORS(app)

# La lógica para encontrar los archivos del padrón sigue siendo la misma
current_dir = os.path.dirname(os.path.abspath(__file__))

def verify_cuit(cuit, jur):
    padron_files = {
        "AGIP": "padron_agip.txt",
        "ARBA": "padron_arba.txt"
    }
    
    file_path = os.path.join(current_dir, padron_files.get(jur))

    if not file_path or not os.path.exists(file_path):
        return {"error": f"Padrón para {jur} no encontrado en el servidor."}

    try:
        df = pd.read_csv(file_path, sep=';', header=None, dtype=str)
        df.columns = ['CUIT', 'Alicuota']
        
        result = df[df['CUIT'] == cuit]
        
        if not result.empty:
            alicuota = result['Alicuota'].iloc[0]
            # ... (El resto de la lógica para construir la respuesta es idéntica)
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
                    "nombre_archivo": os.path.basename(file_path),
                    "fecha_publicacion": "2025-06-15",
                    "enlace_oficial": "#"
                }
            }
        else:
             return {
                "encontrado": False,
                "cuit_consultado": cuit,
                "jurisdiccion": f"{jur}",
                "mensaje": "El CUIT no se encuentra en el padrón. No corresponde aplicar retención."
            }
    except Exception as e:
        return {"error": f"Error procesando el padrón: {str(e)}"}

# Vercel buscará y ejecutará esta variable 'app' de Flask
@app.route('/api/verify', methods=['GET'])
def handle_verify():
    cuit = request.args.get('cuit')
    jur = request.args.get('jur')

    if not cuit or not jur:
        return jsonify({"error": "CUIT y Jurisdicción son requeridos."}), 400
    
    response_data = verify_cuit(cuit, jur)
    return jsonify(response_data)
