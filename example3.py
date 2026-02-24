import json
from openai import OpenAI

class AgenteReact:
    def __init__(self, client, system_prompt, model_id="qwen2-7b-instruct"):
        self.client = client
        self.system_prompt = system_prompt
        self.model_id = model_id
        self.memoria_contextual = [] 

    def agregar_memoria(self, rol, contenido):
        self.memoria_contextual.append({"role": rol, "content": contenido})

    def ejecutar_ciclo(self, tarea_usuario):
        print(f"🚀 Iniciando tarea: {tarea_usuario}")
        self.agregar_memoria("user", tarea_usuario)
        
        max_iteraciones = 5
        for i in range(max_iteraciones):
            respuesta = self.llamar_llm()
            
            if "Acción:" in respuesta:
                accion = self.parsear_accion(respuesta)
                # Limpiamos posibles corchetes que el LLM añada por error
                tool_name = accion['tool'].replace("[", "").replace("]", "").strip()
                
                print(f"🛠️  [Iteración {i+1}] Usando: {tool_name}")
                
                resultado_herramienta = self.ejecutar_herramienta({'tool': tool_name, 'input': accion['input']})
                print(f"🔍 Observación: {resultado_herramienta}")
                
                self.agregar_memoria("assistant", respuesta)
                self.agregar_memoria("user", f"Observación: {resultado_herramienta}")
            else:
                return respuesta
        
        return "⚠️ Límite de razonamiento alcanzado sin solución."

    def llamar_llm(self):
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "system", "content": self.system_prompt}] + self.memoria_contextual,
            temperature=0
        )
        return response.choices[0].message.content

    def parsear_accion(self, respuesta):
        lineas = respuesta.split('\n')
        tool = ""
        inp = ""
        for linea in lineas:
            if "Acción:" in linea:
                tool = linea.split("Acción:")[1].strip()
            if "Input:" in linea:
                inp = linea.split("Input:")[1].strip()
        return {"tool": tool, "input": inp}

    def ejecutar_herramienta(self, accion):
        if accion['tool'] == 'calculadora':
            try:
                # Resolvemos el cálculo matemático
                return eval(accion['input']) 
            except Exception as e:
                return f"Error en el cálculo: {e}"
        return f"Error: Herramienta '{accion['tool']}' no disponible. Usa solo 'calculadora'."
    
        # Herramienta profesional de Vertex
    def calculadora_segura(operacion, a, b):
        """Sustituye la ejecución de strings por funciones lógicas."""
        operaciones = {
            "sumar": a + b,
            "multiplicar": a * b,
            "restar": a - b,
            "dividir": a / b if b != 0 else "Error: Div por cero"
        }
        return operaciones.get(operacion, "Operación no soportada")

    # El Agente ahora debe llamar a la herramienta así:
    # Acción: calculadora_segura
    # Input: {"operacion": "multiplicar", "a": 144, "b": 2}

if __name__ == "__main__":
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    PROMPT_SISTEMA = """Eres un agente de Vertex Coders. Resuelve tareas paso a paso.
    Formato obligatorio:
    Pensamiento: [razonamiento]
    Acción: calculadora
    Input: [operación matemática]
    
    Solo tienes la herramienta: calculadora. Si ya tienes la respuesta final, dila directamente sin usar 'Acción:'."""

    agente = AgenteReact(client, PROMPT_SISTEMA)
    tarea = "¿Cuál es el resultado de multiplicar 144 por 2 y sumarle 56?"
    resultado = agente.ejecutar_ciclo(tarea)
    
    print(f"\n✅ RESULTADO FINAL:\n{resultado}")