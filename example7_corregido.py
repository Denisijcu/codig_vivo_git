import requests
import json
import os

# --- 1. CONFIGURACIÓN DE INFRAESTRUCTURA SOBERANA ---
# Si usas Docker, mantén host.docker.internal; si es local, usa localhost
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

def pensar(sombrero, contexto):
    """Interfaz de comunicación con el cerebro local qwen2-7b-instruct."""
    payload = {
        "model": "qwen2-7b-instruct", # Sincronizado con tu laboratorio
        "messages": [
            {"role": "system", "content": sombrero["rol"]},
            {"role": "user", "content": f"Contexto actual:\n{contexto}\n\nInstrucción: {sombrero['instruccion']}"}
        ],
        "temperature": 0.2, # Rigor técnico máximo para evitar alucinaciones
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, headers=HEADERS, json=payload, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error de conexión: {e}. ¿Está LM Studio encendido?"

# --- 2. PROTOCOLO DE LOS 6 SOMBREROS (VERTEX FRAMEWORK) ---
SOMBREROS = {
    "BLANCO": {
        "rol": "Analista de requisitos. Hechos y datos puros.",
        "instruccion": "Define los requisitos técnicos y funcionales de forma concisa."
    },
    "NEGRO": {
        "rol": "Auditor de Seguridad (Nemesis IA Style).",
        "instruccion": "Identifica riesgos lógicos. Advierte sobre variables no definidas o fugas de datos."
    },
    "VERDE": {
        "rol": "Senior Full Stack Developer.",
        "instruccion": "Escribe el código Python completo, modular y documentado."
    },
    "ROJO": {
        "rol": "QA Tester implacable.",
        "instruccion": "Valida el código. Si hay errores lógicos, responde RECHAZADO y explica por qué."
    },
    "AMARILLO": {
        "rol": "Ingeniero de Optimización.",
        "instruccion": "Refactoriza para legibilidad y limpieza según PEP 8."
    },
    "AZUL": {
        "rol": "CTO de Vertex Coders.",
        "instruccion": "Si el código es óptimo, responde 'APROBADO_FIN'. De lo contrario, pide correcciones."
    }
}

# --- 3. ORQUESTADOR DE LA COLMENA ---
class AgenteMaestro:
    def __init__(self, max_ciclos=2):
        self.max_ciclos = max_ciclos
        self.estado = {}

    def guardar_en_disco(self, codigo, nombre="solucion_vertex.py"):
        """Materializa el código aprobado en un archivo ejecutable."""
        try:
            # Limpieza profesional de bloques Markdown
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
            
            # 1. Análisis de Hechos
            self.estado['req'] = pensar(SOMBREROS["BLANCO"], contexto_problema)
            print("⚪ Sombrero Blanco: OK.")
            
            # 2. Auditoría de Riesgos (Protocolo Némesis)
            self.estado['riesgos'] = pensar(SOMBREROS["NEGRO"], self.estado['req'])
            print("⚫ Sombrero Negro: Riesgos evaluados.")
            
            # 3. Desarrollo
            ctx_dev = f"Reqs: {self.estado['req']}\nRiesgos: {self.estado['riesgos']}"
            self.estado['codigo'] = pensar(SOMBREROS["VERDE"], ctx_dev)
            print("🟢 Sombrero Verde: Código generado.")
            
            # 4. Control de Calidad
            self.estado['qa'] = pensar(SOMBREROS["ROJO"], self.estado['codigo'])
            print(f"🔴 Sombrero Rojo: {self.estado['qa'][:40]}...")
            
            # 5. Optimización PEP 8
            self.estado['final'] = pensar(SOMBREROS["AMARILLO"], self.estado['codigo'])
            print("🟡 Sombrero Amarillo: Refactorizado.")
            
            # 6. Decisión Ejecutiva
            decision = pensar(SOMBREROS["AZUL"], self.estado['final'])
            print(f"🔵 Sombrero Azul (CTO): {decision[:50]}")
            
            if "APROBADO_FIN" in decision.upper():
                print("\n✨ ÉXITO: El CTO ha dado luz verde.")
                return self.guardar_en_disco(self.estado['final'])
            
            # Retroalimentación para el siguiente ciclo si falla
            contexto_problema = f"Tarea: {tarea}\nError detectado: {decision}\nCódigo a mejorar: {self.estado['final']}"

        return "⚠️ Se alcanzó el límite de ciclos sin aprobación. Revisa los logs de seguridad."

if __name__ == "__main__":
    colmena = AgenteMaestro(max_ciclos=2)
    meta = "Crear un script de Python que monitoree el puerto 8080 y bloquee IPs con más de 10 intentos fallidos."
    
    reporte = colmena.ejecutar(meta)
    print(f"\n🏆 RESULTADO:\n{reporte}")