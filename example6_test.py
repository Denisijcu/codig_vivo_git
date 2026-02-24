from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# --- ESCENARIO 1: EL PROMPT SIMPLE (Lo que hace la mayoría) ---
PROMPT_SIMPLE = "Eres un asistente de seguridad. Analiza este log: 'IP 192.168.1.50 intentó 50 logins fallidos'."

# --- ESCENARIO 2: EL PROMPT ESTRUCTURADO (Estándar Vertex Coders) ---
PROMPT_VERTEX = """
IDENTIDAD:
Eres el Agente de Respuesta de Nemesis IA. Tu misión es proteger la infraestructura de Vertex Services.

INSTRUCCIONES DE RAZONAMIENTO:
1. Identifica el tipo de amenaza (Brute Force, SQLi, etc).
2. Determina el nivel de severidad (Bajo, Medio, Alto, Crítico).
3. Propón una acción inmediata (Bloqueo IP, Cambio de Credenciales).

FORMATO DE SALIDA (Obligatorio):
{
  "amenaza": "nombre",
  "severidad": "nivel",
  "accion_sugerida": "descripcion",
  "razonamiento": "breve explicacion"
}
"""

def probar_prompt(nombre, sistema, usuario):
    print(f"\n--- PROBANDO: {nombre} ---")
    try:
        response = client.chat.completions.create(
            model="qwen2-7b-instruct",
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario}
            ],
            temperature=0 # Temperatura baja para análisis técnico
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    log_usuario = "LOG_EVENT: IP 192.168.1.50 - 50 FAILED LOGIN ATTEMPTS IN 2 MINUTES - TARGET: ADMIN_PANEL"
    
    # Prueba 1: El asistente genérico
    probar_prompt("ASISTENTE GENÉRICO", PROMPT_SIMPLE, log_usuario)
    
    # Prueba 2: El Agente Autónomo de Vertex
    probar_prompt("AGENTE NEMESIS IA (ESTRUCTURADO)", PROMPT_VERTEX, log_usuario)