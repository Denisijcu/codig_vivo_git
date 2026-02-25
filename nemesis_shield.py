import requests
import time
import subprocess
import ctypes
import re
from datetime import datetime

# --- CONFIGURACIÓN DE INFRAESTRUCTURA ---
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# --- OPCIONAL: LLM (NO CRÍTICO) ---
def pensar(sombrero, contexto):
    payload = {
        "model": "qwen2-7b-instruct",
        "messages": [
            {"role": "system", "content": sombrero["rol"]},
            {"role": "user", "content": f"Contexto: {contexto}\n\nInstrucción: {sombrero['instruccion']}"}
        ],
        "temperature": 0.1,
    }
    try:
        response = requests.post(LM_STUDIO_URL, headers=HEADERS, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except:
        return "OK"

# --- BLOQUEO REAL EN WINDOWS ---
def bloquear_ip_windows(ip):
    if not ip:
        return False

    rule_name = f"NEMESIS_BLOCK_{ip}"
    comando = [
        "netsh", "advfirewall", "firewall",
        "add", "rule",
        f"name={rule_name}",
        "dir=in",
        "action=block",
        f"remoteip={ip}"
    ]

    try:
        subprocess.run(comando, check=True, capture_output=True)
        print(f"🚨 [NÉMESIS] IP {ip} BLOQUEADA en Firewall.")
        return True
    except Exception as e:
        print(f"❌ Error al bloquear IP {ip}: {e}")
        return False

# --- AGENTE NÉMESIS ---
class NemesisAgente:
    def __init__(self):
        print("🛡️  Iniciando Agente Némesis IA - Guardián de Vertex Services...")
        self.fail_counter = {}

    def extraer_ip(self, log_entry):
        match = re.search(r"ip='([^']+)'", log_entry)
        return match.group(1) if match else None

    def patrullar(self, log_entry):
        print(f"\n🔍 Analizando: {log_entry}")

        ip = self.extraer_ip(log_entry)

        # --- REGLA 1: INYECCIÓN ---
        if "INJECTION_ATTEMPT" in log_entry or "DROP " in log_entry:
            print("🚨 Inyección detectada.")
            bloquear_ip_windows(ip)
            self.registrar_incidente(ip, log_entry)
            return

        # --- REGLA 2: FUERZA BRUTA ---
        if "status='fail'" in log_entry and ip:
            self.fail_counter[ip] = self.fail_counter.get(ip, 0) + 1
            print(f"Intentos fallidos {ip}: {self.fail_counter[ip]}")

            if self.fail_counter[ip] >= 3:
                print("🚨 Ataque de fuerza bruta detectado.")
                bloquear_ip_windows(ip)
                self.registrar_incidente(ip, log_entry)
                return

        # --- REGLA 3: LOGIN EXITOSO ---
        if "status='success'" in log_entry:
            print("✅ Login legítimo.")
            return

        print("✅ Tráfico verificado como seguro.")

    def registrar_incidente(self, ip, detalle):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 Incidente registrado: {ip} a las {timestamp}")

# --- MAIN ---
if __name__ == "__main__":

    # Verificar privilegios admin
    try:
        es_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        es_admin = False

    if not es_admin:
        print("⚠️ Ejecuta este script como ADMINISTRADOR.")

    guardian = NemesisAgente()

    logs_trafico = [
        "USER_LOGIN: user='denis' status='success' ip='192.168.1.10'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "USER_LOGIN: user='admin' status='fail' ip='45.33.22.11'",
        "INJECTION_ATTEMPT: input='DROP TABLE users;' ip='45.33.22.11'"
    ]

    print("\n" + "="*60)
    print("🚀 MONITOREO EN VIVO ACTIVADO")
    print("="*60)

    for entrada in logs_trafico:
        guardian.patrullar(entrada)
        time.sleep(1)

    print("\n✅ Patrullaje finalizado.")