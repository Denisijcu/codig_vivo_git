import json
from openai import OpenAI
from datetime import datetime

# --- 1. Definición de Herramientas (Arsenal) ---
# Usamos un esquema JSON para que el modelo entienda qué datos necesitamos exactamente.
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "crear_cotizacion",
            "description": "Genera una cotización formal para un cliente de Vertex Coders",
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente": {"type": "string", "description": "Nombre del cliente"},
                    "servicios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de servicios contratados"
                    },
                    "precio_total": {"type": "number", "description": "Total en USD"}
                },
                "required": ["cliente", "servicios", "precio_total"]
            }
        }
    }
]

# --- 2. Lógica de Ejecución (Blindaje Técnico) ---
def ejecutar_herramienta(nombre_funcion, argumentos):
    """
    Ejecuta la acción solicitada por la IA con validación de errores.
    """
    try:
        if nombre_funcion == "crear_cotizacion":
            # Validación de argumentos: nos aseguramos de que los datos existan
            cliente = argumentos.get('cliente')
            total = argumentos.get('precio_total')
            
            if not cliente or total is None:
                raise ValueError("Argumentos incompletos para procesar la cotización.")

            # Simulamos la integración con Vertex Systems
            return json.dumps({
                "status": "success", 
                "message": f"Cotización de ${total} enviada a {cliente} vía Vertex Systems"
            })
            
        return json.dumps({"status": "error", "message": "Herramienta no encontrada"})

    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error en ejecución: {str(e)}"})

# --- 3. El Motor de Orquestación ---
if __name__ == "__main__":
    # Conexión soberana a LM Studio
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    
    PROMPT_SISTEMA = "Eres el agente comercial de Vertex Coders. Usa la función crear_cotizacion para gestionar pedidos."

    tarea_usuario = "Hola, soy Denis de Miami. Necesito una cotización para un desarrollo Full Stack y una auditoría de Nemesis IA por 2500 dólares."
    
    print(f"📥 Solicitud: {tarea_usuario}\n")

    try:
        response = client.chat.completions.create(
            model="qwen2-7b-instruct",
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": tarea_usuario}
            ],
            tools=tools_schema,
            tool_choice="auto"
        )

        respuesta_llm = response.choices[0].message

        # Verificamos si el LLM activó una herramienta
        if respuesta_llm.tool_calls:
            for tool_call in respuesta_llm.tool_calls:
                nombre = tool_call.function.name
                
                # Validación del JSON de argumentos
                try:
                    argumentos = json.loads(tool_call.function.arguments)
                    print(f"🛠️  Agente solicita: {nombre}")
                    print(f"📦 Argumentos: {argumentos}")
                    
                    resultado = ejecutar_herramienta(nombre, argumentos)
                    print(f"🔍 Resultado: {resultado}")
                except json.JSONDecodeError:
                    print("🚨 Error: La IA envió un formato de argumentos inválido.")
        else:
            print(f"🤖 Respuesta directa: {respuesta_llm.content}")

    except Exception as e:
        print(f"❌ Error de conexión o modelo: {e}")