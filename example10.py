import os
import re
import faiss
import pickle
import numpy as np
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer

# =========================================
# 🧠 MOTOR DE MEMORIA
# =========================================

class MemoriaAmenazas:
    def __init__(self, index_file="nemesis_memory.index", metadata_file="metadata.pkl"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.dimension = 384

        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, "rb") as f:
                self.metadata = pickle.load(f)
            print("🧠 Memoria cargada.")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            print("🆕 Memoria nueva creada.")

    def guardar_ataque(self, log_entry, ip):
        vector = self.model.encode([log_entry])
        vector = np.array(vector).astype("float32")

        self.index.add(vector)
        self.metadata.append({
            "ip": ip,
            "fecha": str(datetime.now()),
            "log": log_entry
        })

        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "wb") as f:
            pickle.dump(self.metadata, f)

        print("💾 Ataque guardado en memoria.")

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
# 🛡️ AGENTE NÉMESIS
# =========================================

class NemesisAgente:
    def __init__(self):
        print("🛡️ Iniciando Némesis con Memoria Activa...")
        self.memoria = MemoriaAmenazas()
        self.fail_counter = {}
        self.ip_bloqueadas = set()

    def extraer_ip(self, log_entry):
        match = re.search(r"ip='([^']+)'", log_entry)
        return match.group(1) if match else None

    def bloquear_ip(self, ip):
        if not ip:
            return
        if ip in self.ip_bloqueadas:
            return

        print(f"🚨 BLOQUEANDO IP: {ip}")
        self.ip_bloqueadas.add(ip)

    def patrullar(self, log_entry):
        print(f"\n🔍 Analizando: {log_entry}")

        ip = self.extraer_ip(log_entry)

        # 1️⃣ Consultar memoria
        distancia, recuerdo = self.memoria.consultar_similitud(log_entry)

        if distancia is not None and distancia < 0.4:
            print(f"⚠️ ATAQUE RECONOCIDO (dist={distancia:.4f})")
            print(f"Relacionado con IP previa: {recuerdo['ip']}")
            self.bloquear_ip(ip)
            return

        # 2️⃣ Reglas determinísticas
        if "INJECTION_ATTEMPT" in log_entry or "DROP " in log_entry:
            print("🚨 Inyección detectada.")
            self.bloquear_ip(ip)
            self.memoria.guardar_ataque(log_entry, ip)
            return

        if "status='fail'" in log_entry and ip:
            self.fail_counter[ip] = self.fail_counter.get(ip, 0) + 1
            print(f"Intentos fallidos {ip}: {self.fail_counter[ip]}")

            if self.fail_counter[ip] >= 3:
                print("🚨 Fuerza bruta detectada.")
                self.bloquear_ip(ip)
                self.memoria.guardar_ataque(log_entry, ip)
                return

        if "status='success'" in log_entry:
            print("✅ Login legítimo.")
            return

        print("✅ Tráfico normal.")


# =========================================
# 🚀 MAIN
# =========================================

if __name__ == "__main__":

    guardian = NemesisAgente()

    logs_trafico = [
        "USER_LOGIN: user='denis' status='success' ip='192.168.1.10'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "INJECTION_ATTEMPT: input='DROP TABLE users;' ip='45.33.22.11'",
        # Simulamos repetición para probar memoria
        "INJECTION_ATTEMPT: input='DROP TABLE users;' ip='45.33.22.11'"
    ]

    print("\n" + "="*60)
    print("🚀 MONITOREO EN VIVO ACTIVADO")
    print("="*60)

    for entrada in logs_trafico:
        guardian.patrullar(entrada)
        time.sleep(1)

    print("\n✅ Patrullaje finalizado.")