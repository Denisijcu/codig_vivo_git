import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE MEMORIA (FAISS) ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
memoria_texto = []

def guardar_recuerdo(texto):
    vector = embedder.encode([texto])
    index.add(np.array(vector).astype('float32'))
    memoria_texto.append(texto)

def recuperar_contexto(consulta):
    if not memoria_texto: return ""
    vector_consulta = embedder.encode([consulta])
    distancias, indices = index.search(np.array(vector_consulta).astype('float32'), 1)
    recuerdo = memoria_texto[indices[0][0]] if indices[0][0] != -1 else ""
    return f"\nRecuerdo relevante: {recuerdo}"

# --- 2. AGENTE REACT MEJORADO ---
class AgenteConMemoria:
    def __init__(self, client, system_prompt):
        self.client = client
        self.system_prompt = system_prompt

    def ejecutar(self, tarea):
        # El agente "recuerda" antes de pensar
        contexto_extra = recuperar_contexto(tarea)
        prompt_final = self.system_prompt + contexto_extra
        
        print(f"🧠 Contexto recuperado: {contexto_extra or 'Ninguno'}")
        
        response = self.client.chat.completions.create(
            model="qwen2-7b-instruct",
            messages=[
                {"role": "system", "content": prompt_final},
                {"role": "user", "content": tarea}
            ],
            temperature=0
        )
        return response.choices[0].message.content

# --- 3. PRUEBA DE PERSISTENCIA EN VERTEX CODERS ---
if __name__ == "__main__":
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    
    # El agente "aprende" algo hoy
    guardar_recuerdo("El servidor de producción de Vertex Services usa el puerto 8080.")
    
    agente = AgenteConMemoria(client, "Eres un ingeniero de soporte técnico.")
    
    # El usuario pregunta algo relacionado tiempo después
    pregunta = "¿En qué puerto debo configurar el firewall?"
    print(f"👤 Usuario: {pregunta}")
    
    resultado = agente.ejecutar(pregunta)
    print(f"\n🤖 Agente: {resultado}")
