import numpy as np
import faiss
import os
import json
import logging
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# 1. CONFIGURACIÓN DE LOGS (Observabilidad Enterprise)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. CLIENTE SOBERANO
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 3. CLASE MEMORIA VECTORIAL (Persistencia Real) [cite: 8746, 8771]
class MemoriaVectorial:
    def __init__(self, index_path="vertex_memory.index", data_path="vertex_memory.json"):
        self.modelo = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.index_path = index_path
        self.data_path = data_path
        self.textos = []

        if os.path.exists(self.index_path) and os.path.exists(self.data_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.textos = json.load(f)
            logging.info(f"✅ Memoria cargada: {len(self.textos)} recuerdos.")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            logging.info("🆕 Memoria nueva inicializada.")

    def agregar(self, texto):
        vector = self.modelo.encode([texto])
        self.index.add(np.array(vector).astype('float32'))
        self.textos.append(texto)
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.textos, f)

    def recuperar(self, consulta, k=1, threshold=1.2):
        if not self.textos: return ""
        v = self.modelo.encode([consulta])
        distancias, indices = self.index.search(np.array(v).astype('float32'), k)
        
        if distancias[0][0] < threshold and indices[0][0] < len(self.textos):
            return self.textos[indices[0][0]]
        return ""

# 4. CLASE ORQUESTADOR (Lógica Multi-Agente) [cite: 9030, 9080]
class Orquestador:
    def __init__(self, memoria, seguridad, auditor):
        self.memoria = memoria
        self.seguridad = seguridad
        self.auditor = auditor
        self.max_tokens = 6000 # Hardening de ventana [cite: 10185]

    def procesar(self, mensaje):
        # Validación Protocolo Némesis [cite: 9682, 9805]
        if not self.seguridad.validar(mensaje):
            logging.error(f"❌ Bloqueado: {mensaje}")
            return "Petición bloqueada por seguridad."

        # RAG: Recuperación Semántica [cite: 8732]
        contexto = self.memoria.recuperar(mensaje)
        
        # Ejecución en el cerebro local qwen2-7b 
        respuesta = self._ejecutar_agente(mensaje, contexto)
        
        self.auditor.registrar(mensaje, respuesta)
        return respuesta

    def _ejecutar_agente(self, mensaje, contexto):
        try:
            prompt_sistema = f"Eres el experto de Vertex Coders. Usa este contexto: {contexto}"
            response = client.chat.completions.create(
                model="qwen2-7b-instruct",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": mensaje}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error de inferencia: {e}"

# 5. ENTRADA ÚNICA (MAIN RECTIFICADO)
if __name__ == "__main__":
    # Componentes Reales y Mocks de Seguridad
    class SeguridadNemesis:
        def validar(self, msg):
            return not any(p in msg.upper() for p in ["DROP", "DELETE", "GRANT"])

    class AuditorVertex:
        def registrar(self, msg, res):
            logging.info(f"📝 Auditado: {msg[:30]}...")

    # Inicialización del ecosistema
    memoria_real = MemoriaVectorial()
    
    # Alimentar memoria si está vacía
    if not memoria_real.textos:
        memoria_real.agregar("El servidor de Vertex corre en el puerto 8080.")
    
    seguridad = SeguridadNemesis()
    auditor = AuditorVertex()
    
    # Orquestador final
    vertex_system = Orquestador(memoria_real, seguridad, auditor)

    print("\n🚀 --- SISTEMA VERTEX ONLINE ---")
    user_msg = "¿Cuál es el puerto del servidor?"
    print(f"👤 Usuario: {user_msg}")
    print(f"🤖 Agente: {vertex_system.procesar(user_msg)}")