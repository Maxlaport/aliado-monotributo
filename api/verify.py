from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
from urllib.parse import urlparse, parse_qs
import os

# Obtenemos la ruta del directorio actual para poder encontrar los archivos del padrón
current_dir = os.path.dirname(os.path.abspath(__file__))

def verify_cuit(cuit, jur):
    padron_files = {
        "AGIP": "padron_agip.txt",
        "ARBA": "padron_arba.txt"
    }

    file_path = os.path.join(current_dir, padron_files.get(jur))

    if not file_path or not os.path.exists(file_path):
        return {"error": f"Padrón para {jur} no encontrado."}

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
                    "nombre_archivo": os.path.basename(file_path),
                    "fecha_publicacion": "2025-06-15",
                    "enlace_oficial": "#" # En la version real, aqui iria el link
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        cuit = query_params.get('cuit', [None])[0]
        jur = query_params.get('jur', [None])[0]

        if not cuit or not jur:
            response_data = {"error": "CUIT y Jurisdicción son requeridos."}
            status_code = 400
        else:
            response_data = verify_cuit(cuit, jur)
            status_code = 200

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # CORS
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
