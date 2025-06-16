import fs from 'fs/promises';
import path from 'path';

export default async function handler(req, res) {
  const { cuit, jur } = req.query;

  if (!cuit || !jur) {
    return res.status(400).json({ error: "CUIT y Jurisdicción son requeridos." });
  }

  const padronFiles = {
    AGIP: 'padron_agip.txt',
    ARBA: 'padron_arba.txt'
  };

  const filename = padronFiles[jur];
  if (!filename) {
    return res.status(400).json({ error: `Jurisdicción '${jur}' no es válida.` });
  }

  const filePath = path.join(process.cwd(), 'api', filename);

  try {
    const data = await fs.readFile(filePath, 'utf-8');
    const lines = data.split('\n');
    let found = false;
    let alicuota = null;

    for (let line of lines) {
      const [fileCuit, fileAlicuota] = line.trim().split(';');
      if (fileCuit === cuit) {
        found = true;
        alicuota = fileAlicuota;
        break;
      }
    }

    if (found) {
      return res.status(200).json({
        encontrado: true,
        cuit_consultado: cuit,
        jurisdiccion: jur,
        resultado: {
          tipo_alicuota: "Retención/Percepción",
          alicuota: `${alicuota}%`,
          mensaje: `Se debe aplicar una alícuota del ${alicuota}%.`
        },
        fuente_de_datos: {
          nombre_padron: `Padrón de Ejemplo - Junio 2025 (${jur})`,
          nombre_archivo: filename,
          fecha_publicacion: "2025-06-15",
          enlace_oficial: "#"
        }
      });
    } else {
      return res.status(200).json({
        encontrado: false,
        cuit_consultado: cuit,
        jurisdiccion: jur,
        mensaje: "El CUIT no se encuentra en el padrón."
      });
    }
  } catch (err) {
    return res.status(500).json({ error: `Error leyendo el padrón: ${err.message}` });
  }
}
