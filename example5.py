import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# 1. Inicializar el modelo de embeddings (el mismo que usábamos)
# Este modelo convierte texto en una lista de números (vectores)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Configurar el índice de FAISS
# '384' es la dimensión de los vectores que genera el modelo MiniLM
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Memoria persistente simple para guardar el texto original
memoria_texto = []

def guardar_recuerdo(texto):
    """ Convierte texto a vector y lo guarda en el índice """
    # Convertimos el texto a vector
    vector = embedder.encode([texto])
    # Agregamos al índice de FAISS
    index.add(np.array(vector).astype('float32'))
    # Guardamos el texto para poder recuperarlo luego
    memoria_texto.append(texto)
    print(f"✅ Recuerdo guardado: {texto[:50]}...")

def recuperar_recuerdos(consulta, n_resultados=1):
    """ Busca los recuerdos más cercanos vectorialmente """
    vector_consulta = embedder.encode([consulta])
    # FAISS busca los 'n' vectores más parecidos
    distancias, indices = index.search(np.array(vector_consulta).astype('float32'), n_resultados)
    
    resultados = []
    for i in indices[0]:
        if i != -1: # -1 significa que no encontró nada
            resultados.append(memoria_texto[i])
    return resultados

# --- Prueba en vivo ---
if __name__ == "__main__":
    guardar_recuerdo("El cliente prefiere auditorías con Nemesis IA los lunes.")
    
    print("\n🔍 Consultando memoria...")
    recuerdos = recuperar_recuerdos("¿Cuándo prefiere el cliente las auditorías?")
    print(f"🤖 El agente recuerda: {recuerdos}")