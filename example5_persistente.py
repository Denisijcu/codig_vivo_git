import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

# Configuración de archivos
INDEX_FILE = "vertex_memory.index"
DATA_FILE = "vertex_memory.json"

encoder = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384 

# 1. Cargar o Inicializar la Memoria
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        memoria_texto = json.load(f)
    print("🧠 Memoria cargada desde el disco.")
else:
    index = faiss.IndexFlatL2(dimension)
    memoria_texto = []
    print("🆕 Nueva memoria inicializada.")

def guardar_memoria_total(texto):
    """Guarda el recuerdo y lo persiste inmediatamente en el disco."""
    # Guardar en RAM
    vector = encoder.encode([texto])
    index.add(np.array(vector).astype('float32'))
    memoria_texto.append(texto)
    
    # Persistir en disco (Vertex Protocol)
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria_texto, f)
    
    print(f"💾 Recuerdo persistido: {texto[:40]}...")

def buscar_recuerdo(consulta, top_k=1):
    """Busca en el índice persistente."""
    if not memoria_texto:
        return []
    
    vector_busqueda = encoder.encode([consulta])
    _, indices = index.search(np.array(vector_busqueda).astype('float32'), top_k)
    
    return [memoria_texto[i] for i in indices[0] if i != -1]

# --- PRUEBA DE PERSISTENCIA ---
if __name__ == "__main__":
    # Si es la primera vez, guarda algo
    if not memoria_texto:
        guardar_memoria_total("Cotización de $2500 para Denis en Miami.")
    
    # Prueba la recuperación
    res = buscar_recuerdo("¿Cuánto se le coticó a Denis?")
    print(f"\n🔍 Resultado de búsqueda persistente: {res}")
