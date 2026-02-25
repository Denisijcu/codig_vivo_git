import os
import faiss
import pickle
import numpy as np
import re
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer

# =========================================
# 🧠 MOTOR DE MEMORIA VERTEX
# =========================================

class MemoriaAmenazas:
    def __init__(self, index_file="nemesis_memory.index", metadata_file="metadata.pkl"):
        # Usamos rutas relativas para máxima portabilidad
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.index_file = os.path.join(self.base_path, index_file)
        self.metadata_file = os.path.join(self.base_path, metadata_file)
        
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, "rb") as f:
                self.metadata = pickle.load(f)
            print("🧠 Memoria cargada: El Guardián recuerda ataques pasados.")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            print("🆕 Memoria nueva: El Guardián está listo para aprender.")

    def guardar_ataque(self, log_entry, ip):
        vector = self.model.encode([log_entry])
        vector = np.array(vector).astype("float32")

        self.index.add(vector)
        self.metadata.append({
            "ip": ip,
            "fecha": str(datetime.now()),
            "log": log_entry
        })

        # Persistencia inmediata en disco
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "wb") as f:
            pickle.dump(self.metadata, f)
        print("💾 Incidente guardado en la memoria de largo plazo.")

    def consultar_similitud(self, log_entry):
        if self.index.ntotal == 0:
            return None, None

        vector = self.model.encode([log_entry])
        vector = np.array(vector).astype("float32")
        distancias, indices = self.index.search(vector, 1)

        idx = indices[0][0]
        distancia = distancias[0][0]

        if idx < 0 or idx >= len(self.metadata):
            return None, None

        return distancia, self.metadata[idx]

# =========================================
# 🛡️ AGENTE NÉMESIS CON MEMORIA ACTIVA
# =========================================

class NemesisAgente:
    def __init__(self):
        print("🛡️ Iniciando Protocolo Némesis...")
        self.memoria = MemoriaAmenazas()
        self.ip_bloqueadas = set()

    def extraer_ip(self, log_entry):
        match = re.search(r"ip='([^']+)'", log_entry)
        return match.group(1) if match else None

    def bloquear_ip_universal(self, ip):
        """Bloqueo multiplataforma (Windows/Linux)"""
        if not ip or ip in self.ip_bloqueadas: return
        
        print(f"🚨 ACCIÓN DISCIPLINARIA: Bloqueando {ip}")
        # Aquí integrarías los comandos netsh (Win) o iptables (Linux)
        self.ip_bloqueadas.add(ip)

    def patrullar(self, log_entry):
        print(f"\n🔍 Analizando: {log_entry}")
        ip = self.extraer_ip(log_entry)

        # 1️⃣ PRIMER PASO: Consultar Memoria (Eficiencia total)
        distancia, recuerdo = self.memoria.consultar_similitud(log_entry)

        if distancia is not None and distancia < 0.4:
            print(f"⚠️ ATAQUE RECONOCIDO (Similitud: {distancia:.4f})")
            print(f"Patrón detectado previamente de la IP: {recuerdo['ip']}")
            self.bloquear_ip_universal(ip)
            return

        # 2️⃣ SEGUNDO PASO: Si es nuevo, aplicar reglas del Cap 9
        if "INJECTION_ATTEMPT" in log_entry or "DROP " in log_entry:
            print("🚨 Inyección detectada por reglas estáticas.")
            self.bloquear_ip_universal(ip)
            self.memoria.guardar_ataque(log_entry, ip) # Aprender del nuevo ataque
            return

        print("✅ Tráfico normal.")

# =========================================
# 🚀 EJECUCIÓN DEL SISTEMA
# =========================================

if __name__ == "__main__":
    guardian = NemesisAgente()
    
    logs = [
        "USER_LOGIN: user='denis' status='success' ip='192.168.1.10'",
        "INJECTION_ATTEMPT: input='DROP TABLE users;' ip='45.33.22.11'",
        # Ataque similar pero no idéntico
        "INJECTION_ATTEMPT: input='DROP TABLE clientes --' ip='45.33.22.11'"
    ]

    for entrada in logs:
        guardian.patrullar(entrada)
        time.sleep(1)