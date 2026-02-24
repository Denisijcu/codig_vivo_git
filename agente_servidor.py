from flask import Flask, request, jsonify, render_template # Añadimos render_template
from flask_cors import CORS 
from example7_corregido import AgenteMaestro

app = Flask(__name__)
CORS(app) 

colmena = AgenteMaestro(max_ciclos=2)

# --- NUEVA RUTA PARA EL FRONTEND ---
@app.route('/')
def home():
    """Sirve la interfaz de control de Vertex."""
    return render_template('index.html')

@app.route('/ejecutar', methods=['POST'])
def ejecutar_colmena():
    datos = request.get_json(force=True)
    tarea = datos.get("tarea")

    if not tarea:
        return jsonify({"error": "No se proporcionó una tarea"}), 400

    print(f"📡 Petición recibida vía Web: {tarea}")
    
    try:
        codigo_aprobado = colmena.ejecutar(tarea)
        return jsonify({
            "status": "success",
            "resultado": codigo_aprobado
        })
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == "__main__":
    # Ahora al correrlo, simplemente vas a http://localhost:5000 en tu navegador
    app.run(host='0.0.0.0', port=5000, debug=True)