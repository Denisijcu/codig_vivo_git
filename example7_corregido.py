import requests
import json
import os

# --- CONFIGURACIÓN DE INFRAESTRUCTURA ---
LM_STUDIO_URL = "http://host.docker.internal:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

def pensar(sombrero, contexto):
    """Interfaz de comunicación con el cerebro local Qwen 2.5."""
    payload = {
        "model": "qwen2-7b-instruct",
        "messages": [
            {"role": "system", "content": sombrero["rol"]},
            {"role": "user", "content": f"Contexto actual:\n{contexto}\n\nInstrucción: {sombrero['instruccion']}"}
        ],
        "temperature": 0.2, # Rigor técnico máximo
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, headers=HEADERS, json=payload, timeout=90)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error de conexión: {e}"

# --- PROTOCOLO DE LOS 6 SOMBREROS (PROMPTS REFINADOS) ---
SOMBREROS = {
    "BLANCO": {
        "rol": "Analista de requisitos. Hechos y datos puros.",
        "instruccion": "Define los requisitos técnicos y funcionales de forma concisa."
    },
    "NEGRO": {
        "rol": "Auditor de Seguridad (Nemesis IA Style).",
        "instruccion": "Identifica riesgos lógicos o de seguridad. Advierte sobre variables no definidas."
    },
    "VERDE": {
        "rol": "Senior Full Stack Developer.",
        "instruccion": "Escribe el código Python completo, modular y documentado."
    },
    "ROJO": {
        "rol": "QA Tester implacable.",
        "instruccion": "Valida el código. Si detectas variables fantasma o errores, responde RECHAZADO."
    },
    "AMARILLO": {
        "rol": "Ingeniero de Optimización.",
        "instruccion": "Refactoriza para legibilidad, eficiencia y limpieza según PEP 8."
    },
    "AZUL": {
        "rol": "CTO de Vertex Coders.",
        "instruccion": "Si el código es óptimo, responde 'APROBADO_FIN'. De lo contrario, pide correcciones."
    }
}

class AgenteMaestro:
    def __init__(self, max_ciclos=2):
        self.max_ciclos = max_ciclos
        self.estado = {}

    def guardar_en_disco(self, codigo, nombre="solucion_vertex.py"):
        """Materializa el pensamiento de la IA en un archivo real."""
        try:
            # Limpiamos el código de posibles bloques de Markdown (```python ... ```)
            if "```python" in codigo:
                codigo = codigo.split("```python")[1].split("```")[0].strip()
            elif "```" in codigo:
                codigo = codigo.split("```")[1].split("```")[0].strip()
            
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(codigo)
            return f"\n💾 ARCHIVO GENERADO: {os.path.abspath(nombre)}"
        except Exception as e:
            return f"\n❌ Error al guardar archivo: {e}"

    def ejecutar(self, tarea):
        print("🚀 INICIANDO PROTOCOLO DE LA COLMENA VERTEX...\n")
        
        contexto_problema = tarea
        for ciclo in range(1, self.max_ciclos + 1):
            print(f"--- 🔄 CICLO DE REFINAMIENTO {ciclo} ---")
            
            # Flujo de trabajo orquestado paso a paso
            self.estado['req'] = pensar(SOMBREROS["BLANCO"], contexto_problema)
            print("⚪ Sombrero Blanco: OK.")
            
            self.estado['riesgos'] = pensar(SOMBREROS["NEGRO"], self.estado['req'])
            print("⚫ Sombrero Negro: Riesgos detectados.")
            
            ctx_dev = f"Reqs: {self.estado['req']}\nRiesgos: {self.estado['riesgos']}"
            self.estado['codigo'] = pensar(SOMBREROS["VERDE"], ctx_dev)
            print("🟢 Sombrero Verde: Código generado.")
            
            self.estado['qa'] = pensar(SOMBREROS["ROJO"], self.estado['codigo'])
            print(f"🔴 Sombrero Rojo: {self.estado['qa'][:30]}...")
            
            self.estado['final'] = pensar(SOMBREROS["AMARILLO"], self.estado['codigo'])
            print("🟡 Sombrero Amarillo: Optimizado.")
            
            decision = pensar(SOMBREROS["AZUL"], self.estado['final'])
            print(f"🔵 Sombrero Azul (CTO): {decision[:50]}")
            
            if "APROBADO_FIN" in decision.upper():
                print("\n✨ ÉXITO: El CTO ha dado luz verde.")
                reporte_disco = self.guardar_en_disco(self.estado['final'])
                print(reporte_disco)
                return self.estado['final']
            
            contexto_problema = f"Error previo: {decision}. Refactorizar código: {self.estado['final']}"

        return "⚠️ Se alcanzó el límite de ciclos sin aprobación final."

if __name__ == "__main__":
    colmena = AgenteMaestro(max_ciclos=2)
    meta = "Crear un sistema de detección de anomalías usando IsolationForest para transacciones financieras."
    
    codigo_aprobado = colmena.ejecutar(meta)
    print("\n🏆 RESULTADO FINAL EN TERMINAL:\n" + "="*40 + "\n" + codigo_aprobado)