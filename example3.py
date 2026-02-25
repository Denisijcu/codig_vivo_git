import json
import re
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROMPT_SISTEMA = """
Eres un agente de Vertex Coders.

Responde SIEMPRE en formato JSON válido.
Nunca uses bloques markdown (no uses ```json).
Nunca escribas texto fuera del JSON.

Si necesitas usar una herramienta:
{
  "thought": "razonamiento interno",
  "action": "calculadora_segura",
  "input": {
    "operacion": "sumar|restar|multiplicar|dividir",
    "a": numero,
    "b": numero
  }
}

Si ya tienes la respuesta final:
{
  "final_answer": "resultado final explicado"
}
"""


class AgenteReactSeguro:
    def __init__(self, client: OpenAI, model_id: str = "qwen2-7b-instruct"):
        self.client = client
        self.model_id = model_id

        # Mapa de herramientas permitidas
        self._herramientas = {
            "calculadora_segura": self._calculadora_segura
        }

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------

    def _llamar_llm(self, memoria: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "system", "content": PROMPT_SISTEMA}] + memoria,
            temperature=0
        )
        return response.choices[0].message.content

    # --------------------------------------------------
    # PARSEO: strip markdown por si el modelo lo ignora
    # --------------------------------------------------

    def _parsear_json(self, texto: str) -> dict:
        texto_limpio = re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", texto, flags=re.DOTALL).strip()
        try:
            data = json.loads(texto_limpio)
            if not isinstance(data, dict):
                raise ValueError("La respuesta no es un objeto JSON.")
            return data
        except Exception:
            logging.error(f"JSON inválido recibido:\n{texto}")
            raise ValueError(f"Respuesta inválida del modelo:\n{texto}")

    # --------------------------------------------------
    # HERRAMIENTAS
    # --------------------------------------------------

    def _ejecutar_herramienta(self, tool_name: str, params: dict):
        handler = self._herramientas.get(tool_name)
        if not handler:
            raise ValueError(f"Herramienta '{tool_name}' no permitida.")
        return handler(params)

    def _calculadora_segura(self, params: dict):
        operacion = params.get("operacion")
        a = params.get("a")
        b = params.get("b")

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return "Error: parámetros inválidos."

        ops = {
            "sumar":       lambda: a + b,
            "restar":      lambda: a - b,
            "multiplicar": lambda: a * b,
            "dividir":     lambda: a / b if b != 0 else "Error: división por cero"
        }

        fn = ops.get(operacion)
        return fn() if fn else "Operación no soportada."

    # --------------------------------------------------
    # CICLO PRINCIPAL
    # memoria local → no se contamina entre llamadas
    # --------------------------------------------------

    def ejecutar(self, tarea: str) -> str:
        logging.info(f"Iniciando tarea: {tarea}")

        memoria = [{"role": "user", "content": tarea}]

        for iteracion in range(1, 7):
            raw = self._llamar_llm(memoria)

            try:
                data = self._parsear_json(raw)
            except ValueError as e:
                return str(e)

            # Respuesta final
            if "final_answer" in data:
                logging.info("✅ Respuesta final alcanzada.")
                return data["final_answer"]

            # Acción
            if "action" in data:
                thought = data.get("thought", "")
                tool = data["action"]
                params = data.get("input", {})

                if thought:
                    logging.info(f"[{iteracion}] Thought: {thought}")
                logging.info(f"[{iteracion}] Tool: {tool} | Params: {params}")

                try:
                    resultado = self._ejecutar_herramienta(tool, params)
                except ValueError as e:
                    return str(e)

                logging.info(f"[{iteracion}] Resultado: {resultado}")

                memoria.append({"role": "assistant", "content": raw})
                memoria.append({"role": "user", "content": f"Observación: {resultado}"})
            else:
                return "⚠️ Formato inesperado del modelo."

        return "⚠️ Límite de iteraciones alcanzado."


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

    agente = AgenteReactSeguro(client)

    resultado = agente.ejecutar("¿Cuál es el resultado de multiplicar 144 por 2 y sumarle 56?")

    print("\n✅ RESULTADO FINAL:")
    print(resultado)