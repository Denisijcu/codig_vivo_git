import numpy as np
import faiss
import os
import json
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE INFRAESTRUCTURA ---
INDEX_FILE = "vertex_memory.index"
DATA_FILE = "vertex_memory.json"
embedder = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

def inicializar_memoria(limpiar=False):
    if limpiar and os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
        os.remove(DATA_FILE)
        print("🧹 Memoria reseteada.")
    
    if os.path.exists(INDEX_FILE) and os.path.exists(DATA_FILE):
        idx = faiss.read_index(INDEX_FILE)
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            txt = json.load(f)
        return idx, txt
    else:
        return faiss.IndexFlatL2(dimension), []

def guardar_recuerdo(texto, index, memoria_texto):
    vector = embedder.encode([texto])
    index.add(np.array(vector).astype('float32'))
    memoria_texto.append(texto)
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria_texto, f)
    print(f"💾 Dato técnico guardado: {texto}")

def recuperar_contexto(consulta, index, memoria_texto, threshold=1.4):
    if not memoria_texto: return ""
    v = embedder.encode([consulta])
    distancias, indices = index.search(np.array(v).astype('float32'), 1)
    
    if distancias[0][0] < threshold and indices[0][0] != -1:
        return f"\n[MANUAL TÉCNICO VERTEX]: {memoria_texto[indices[0][0]]}"
    return ""

# --- 2. LÓGICA DEL AGENTE ---
class AgenteVertex:
    def __init__(self, client, system_prompt):
        self.client = client
        self.system_prompt = system_prompt

    def ejecutar(self, tarea, index, memoria_texto):
        contexto = recuperar_contexto(tarea, index, memoria_texto)
        # Inyectamos el contexto directamente en la misión
        prompt_final = f"{self.system_prompt}\n{contexto}"
        
        print(f"🧠 FAISS: {'Dato recuperado e inyectado' if contexto else 'Sin datos relevantes'}")
        
        response = self.client.chat.completions.create(
            model="qwen2-7b-instruct", # Tu modelo de laboratorio [cite: 8391]
            messages=[
                {"role": "system", "content": prompt_final},
                {"role": "user", "content": tarea}
            ],
            temperature=0
        )
        return response.choices[0].message.content

# --- 3. EJECUCIÓN ---
if __name__ == "__main__":
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    
    # 1. Inicializar (Cambia a True solo si quieres borrar todo lo anterior)
    index, memoria_texto = inicializar_memoria(limpiar=False)
    
    # 2. Asegurar el dato (Esto garantiza que el puerto 8080 esté en el disco)
    if "puerto 8080" not in str(memoria_texto):
        guardar_recuerdo("El servidor principal de Vertex Coders utiliza el puerto 8080 para todas las comunicaciones.", index, memoria_texto)

    # 3. Nuevo Prompt S.T.A.R. (Más "colaborativo")
    PROMPT_SISTEMA = """Eres el Agente de Soporte de Vertex Coders. 
    Tu misión es informar al usuario basándote en el [MANUAL TÉCNICO VERTEX] proporcionado.
    Si el manual contiene la respuesta, dila con confianza. 
    Si el manual está vacío o no tiene relación, di que necesitas más datos."""

    agente = AgenteVertex(client, PROMPT_SISTEMA)
    
    pregunta = "¿En qué puerto corre el servidor de Vertex?"
    print(f"\n👤 Usuario: {pregunta}")
    print(f"🤖 Agente: {agente.ejecutar(pregunta, index, memoria_texto)}")