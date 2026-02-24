import requests
import json

class CerebroLocal:
    def __init__(self, model_id="qwen2-7b-instruct"):
        # El nuevo endpoint nativo de LM Studio
        self.url = "http://localhost:1234/api/v1/chat"
        self.headers = {"Content-Type": "application/json"}
        self.model_id = model_id

    def pensar(self, prompt_usuario, sistema="Eres un agente de Vertex Coders"):
        # Estructura EXACTA según la última actualización de LM Studio
        payload = {
            "model": self.model_id,
            "system_prompt": sistema,
            "input": prompt_usuario,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status() 
            
            data = response.json()
            
            # Según tu salida de terminal, la respuesta viene en 'output'
            # que es una lista de objetos. Accedemos al contenido del primero.
            if 'output' in data and len(data['output']) > 0:
                return data['output'][0].get('content', 'Sin contenido')
            else:
                return f"Error: Estructura de respuesta desconocida: {data}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Error: No se pudo conectar. Verifica que LM Studio tenga el servidor activo en el puerto 1234."
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

# --- Prueba de Fuego ---
if __name__ == "__main__":
    # Instanciamos con el modelo que tienes cargado
    cerebro = CerebroLocal(model_id="qwen2-7b-instruct")
    
    print("🚀 Consultando al cerebro local (API Nativa)...")
    pregunta = "¿Cómo defines la autonomía de un agente en el proyecto Código Vivo?"
    
    respuesta = cerebro.pensar(
        pregunta,
        sistema="Eres un ingeniero experto en IA y ciberseguridad."
    )
    
    print(f"\n🤖 RESPUESTA:\n{respuesta}")