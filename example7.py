import requests
import json
import time

LM_STUDIO_URL = "http://localhost:1234/api/v1/chat"
HEADERS = {"Content-Type": "application/json"}




# Creamos una sesión global para reutilizar la conexión TCP y ganar velocidad
session = requests.Session()

def pensar(sombrero, contexto, intentos=3):
    """
    Función de comunicación agéntica con gestión avanzada de Timeouts.
    Optimizada para la carga de trabajo de Vertex Services.
    """
    payload = {
        "model": "qwen2-7b-instruct",
        "system_prompt": sombrero["rol"],
        "input": f"Contexto actual:\n{contexto}\n\nInstrucción: {sombrero['instruccion']}",
        "temperature": 0.5
    }
    
    # Aumentamos el timeout a 300 segundos (5 minutos) 
    # Algunos modelos locales cuantizados pueden ser lentos en hardware doméstico
    TIMEOUT_ESPERA = 300 

    for i in range(intentos):
        try:
            # Usamos la sesión y un timeout generoso
            response = session.post(
                LM_STUDIO_URL, 
                headers=HEADERS, 
                json=payload, 
                timeout=TIMEOUT_ESPERA
            )
            response.raise_for_status()
            data = response.json()
            
            if 'output' in data and len(data['output']) > 0:
                return data['output'][0]['content']
            else:
                print(f"⚠️ Intento {i+1}: LM Studio devolvió JSON pero sin 'output'.")
                
        except requests.exceptions.Timeout:
            print(f"🕒 Intento {i+1}: ¡Timeout alcanzado! El modelo está tardando demasiado.")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Intento {i+1}: Error de conexión. ¿LM Studio se cerró?")
        except Exception as e:
            print(f"❌ Intento {i+1}: Error inesperado: {e}")
        
        # Espera exponencial: cada reintento espera un poco más
        tiempo_espera = (i + 1) * 3
        print(f"⏳ Reintentando en {tiempo_espera}s...")
        time.sleep(tiempo_espera)
            
    return "❌ ERROR CRÍTICO: La Colmena no pudo obtener respuesta del cerebro local."
# Definición de los 6 Sombreros (Prompts de Ingeniería)
SOMBREROS = {
    "BLANCO": {
        "rol": "Analista de requisitos. Hechos puros.",
        "instruccion": "Define los requisitos técnicos. Listado conciso."
    },
    "NEGRO": {
        "rol": "Experto en Ciberseguridad (Nemesis IA Style).",
        "instruccion": "Lista 3 fallos críticos o vulnerabilidades a evitar."
    },
    "VERDE": {
        "rol": "Full Stack Developer Senior.",
        "instruccion": "Escribe el código solución robusto y documentado."
    },
    "ROJO": {
        "rol": "QA Tester exigente.",
        "instruccion": "Revisa el código. ¿Es legible? Responde APROBADO o RECHAZADO con errores."
    },
    "AMARILLO": {
        "rol": "Ingeniero de Optimización.",
        "instruccion": "Refactoriza el código para que sea eficiente y Pythonico."
    },
    "AZUL": {
        "rol": "CTO de Vertex Coders.",
        "instruccion": "Evalúa la solución final. Responde 'FIN' o 'REINTENTAR'."
    }
}

class AgenteMaestro:
    def __init__(self, max_ciclos=2):
        self.max_ciclos = max_ciclos
        self.estado = {}

    def ejecutar(self, problema):
        print("🚀 INICIANDO PROTOCOLO DE 6 SOMBREROS CUÁNTICOS...\n")
        
        for ciclo in range(1, self.max_ciclos + 1):
            print(f"--- 🔄 CICLO DE REFINAMIENTO {ciclo} ---")
            
            # Flujo de trabajo orquestado
            self.estado['requisitos'] = pensar(SOMBREROS["BLANCO"], problema)
            print("⚪ Sombrero Blanco: Requisitos definidos.")
            
            self.estado['riesgos'] = pensar(SOMBREROS["NEGRO"], self.estado['requisitos'])
            print("⚫ Sombrero Negro: Riesgos de seguridad identificados.")
            
            contexto_código = f"Requisitos: {self.estado['requisitos']}\nRiesgos: {self.estado['riesgos']}"
            self.estado['código'] = pensar(SOMBREROS["VERDE"], contexto_código)
            print("🟢 Sombrero Verde: Código base generado.")
            
            self.estado['validacion'] = pensar(SOMBREROS["ROJO"], self.estado['código'])
            print(f"🔴 Sombrero Rojo: {self.estado['validacion'][:40]}...")
            
            self.estado['codigo_final'] = pensar(SOMBREROS["AMARILLO"], self.estado['código'])
            print("🟡 Sombrero Amarillo: Optimización aplicada.")
            
            decision = pensar(SOMBREROS["AZUL"], self.estado['codigo_final'])
            print(f"🔵 Sombrero Azul (CTO): {decision}")
            
            if "FIN" in decision.upper():
                print("\n✨ ÉXITO: El Director ha aprobado el código.")
                return self.estado['codigo_final']
            
            problema = f"Feedback del CTO: {decision}. Código previo: {self.estado['codigo_final']}"

        return self.estado['codigo_final']

if __name__ == "__main__":
    agente = AgenteMaestro(max_ciclos=2)
    tarea = "Función en Python para detectar fraudes en transacciones financieras."
    resultado = agente.ejecutar(tarea)
    print("\n🏆 CÓDIGO FINAL GENERADO:\n" + "="*30 + "\n" + resultado)