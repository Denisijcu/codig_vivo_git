import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- CONFIGURACIÓN DE ENTORNO ---
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
encoder = SentenceTransformer('all-MiniLM-L6-v2')
INDEX_FILE = "vertex_memory.index"
DATA_FILE = "vertex_memory.json"

# --- PROMPT MAESTRO (S.T.A.R. FRAMEWORK) ---
PROMPT_SISTEMA_MAESTRO = """
IDENTIDAD:
Eres el Agente de Comunicaciones de Vertex Coders. Tu función es redactar informes técnicos precisos.

CONTEXTO RECUPERADO (MEMORIA VECTORIAL):
{contexto_memoria}

REGLAS DE OPERACIÓN:
1. No utilices lenguaje coloquial ni muletillas.
2. Basate exclusivamente en el contexto proporcionado.
3. Si la información no está en el contexto, responde: {{"error": "Datos insuficientes"}}.

FORMATO DE SALIDA (ESTRICTO JSON):
{{
  "id_reporte": "VTX-99",
  "asunto": "Resumen técnico",
  "cuerpo": "Descripción detallada",
  "nivel_prioridad": "bajo/medio/alto"
}}
"""

# --- FUNCIONES DE APOYO (CAPÍTULO 5) ---
def buscar_recuerdo(consulta, top_k=2):
    if not os.path.exists(INDEX_FILE):
        return []
    index = faiss.read_index(INDEX_FILE)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        memoria_texto = json.load(f)
    
    vector_busqueda = encoder.encode([consulta])
    _, indices = index.search(np.array(vector_busqueda).astype('float32'), top_k)
    return [memoria_texto[i] for i in indices[0] if i != -1]

# --- FUNCIÓN PRINCIPAL DEL CAPÍTULO 6 ---
def generar_reporte_profesional(pregunta_usuario):
    # 1. Recuperación Semántica
    recuerdos = buscar_recuerdo(pregunta_usuario)
    contexto = "\n".join(recuerdos) if recuerdos else "No hay antecedentes en memoria."
    
    # 2. Construcción del Prompt con el Contexto Inyectado
    prompt_formateado = PROMPT_SISTEMA_MAESTRO.format(contexto_memoria=contexto)
    
    print("📡 Consultando al Cerebro Local con contexto recuperado...")
    
    try:
        response = client.chat.completions.create(
            model="qwen2-7b-instruct",
            messages=[
                {"role": "system", "content": prompt_formateado},
                {"role": "user", "content": f"Genera un reporte basado en: {pregunta_usuario}"}
            ],
            temperature=0 # Determinismo máximo
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en la generación: {e}"

# --- ENTRADA MAIN PARA PRUEBAS ---
if __name__ == "__main__":
    print("--- SISTEMA DE REPORTES VERTEX CODERS ---")
    
    # Tarea: El usuario pregunta por algo que guardamos en el Cap 5 (Denis/Cotización)
    pregunta = "¿Cuál es el estatus de la cotización de Denis de Miami?"
    
    reporte_final = generar_reporte_profesional(pregunta)
    
    print("\n✅ REPORTE GENERADO (JSON):")
    print(reporte_final)
