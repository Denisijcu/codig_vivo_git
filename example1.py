from openai import OpenAI

# Conexión al cerebro local
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio" 
)

def pensar(prompt, contexto_sistema="Eres un asistente útil"):
    try:
        response = client.chat.completions.create(
            # CAMBIO AQUÍ: Usa el nombre exacto que aparece en tu terminal
            model="qwen2-7b-instruct", 
            messages=[
                {"role": "system", "content": contexto_sistema},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con el cerebro local: {e}"

# Ejecución del ejemplo
print(pensar("¿Cuál es el sentido de la vida para un agente IA?"))