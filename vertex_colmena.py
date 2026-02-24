import requests
import json
import os
import argparse
from datetime import datetime

# PDF (OBLIGATORIO usar platypus correctamente)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch


# -------------------------------
# CONFIGURACIÓN LM STUDIO
# -------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}
MODEL_ID = "qwen2-7b-instruct"


# -------------------------------
# FUNCIÓN DE COMUNICACIÓN LLM
# -------------------------------
def pensar(sombrero, contexto):
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": sombrero["rol"]},
            {
                "role": "user",
                "content": f"Contexto actual:\n{contexto}\n\nInstrucción: {sombrero['instruccion']}"
            }
        ],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error de conexión con LM Studio: {e}"


# -------------------------------
# SOMBREROS
# -------------------------------
SOMBREROS = {
    "BLANCO": {
        "rol": "Analista de requisitos técnico.",
        "instruccion": "Define requisitos técnicos y funcionales claros."
    },
    "NEGRO": {
        "rol": "Auditor de seguridad.",
        "instruccion": "Identifica riesgos, errores lógicos y variables no definidas."
    },
    "VERDE": {
        "rol": "Senior Python Developer.",
        "instruccion": "Escribe el código Python completo, modular, documentado y funcional."
    },
    "ROJO": {
        "rol": "QA Tester implacable.",
        "instruccion": "Valida el código. Si hay errores responde RECHAZADO."
    },
    "AMARILLO": {
        "rol": "Ingeniero de Optimización.",
        "instruccion": "Refactoriza siguiendo PEP8 y buenas prácticas."
    },
    "AZUL": {
        "rol": "CTO.",
        "instruccion": "Si el código es correcto responde APROBADO_FIN."
    }
}


# -------------------------------
# CLASE AGENTE
# -------------------------------
class AgenteMaestro:

    def __init__(self, max_ciclos=2):
        self.max_ciclos = max_ciclos
        self.estado = {}

    def limpiar_codigo(self, codigo):
        if "```python" in codigo:
            codigo = codigo.split("```python")[1].split("```")[0].strip()
        elif "```" in codigo:
            codigo = codigo.split("```")[1].split("```")[0].strip()
        return codigo

    def guardar_codigo(self, codigo, nombre):
        codigo_limpio = self.limpiar_codigo(codigo)

        with open(nombre, "w", encoding="utf-8") as f:
            f.write(codigo_limpio)

        return os.path.abspath(nombre)

    def generar_pdf(self, contenido, nombre_pdf):
        doc = SimpleDocTemplate(nombre_pdf)
        elements = []

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]

        code_style = ParagraphStyle(
            "CodeStyle",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=8,
            textColor=colors.black
        )

        elements.append(Paragraph("Vertex Coders LLC - Generación Autónoma", normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Preformatted(contenido, code_style))

        doc.build(elements)
        return os.path.abspath(nombre_pdf)

    def ejecutar(self, tarea):
        print("\n🚀 INICIANDO PROTOCOLO VERTEX\n")

        contexto = tarea

        for ciclo in range(1, self.max_ciclos + 1):
            print(f"🔄 CICLO {ciclo}")

            self.estado["req"] = pensar(SOMBREROS["BLANCO"], contexto)
            self.estado["riesgos"] = pensar(SOMBREROS["NEGRO"], self.estado["req"])

            ctx_dev = f"Requisitos:\n{self.estado['req']}\n\nRiesgos:\n{self.estado['riesgos']}"
            self.estado["codigo"] = pensar(SOMBREROS["VERDE"], ctx_dev)

            self.estado["qa"] = pensar(SOMBREROS["ROJO"], self.estado["codigo"])
            self.estado["final"] = pensar(SOMBREROS["AMARILLO"], self.estado["codigo"])

            decision = pensar(SOMBREROS["AZUL"], self.estado["final"])

            print(f"CTO dice: {decision}")

            if "APROBADO_FIN" in decision.upper():
                print("✅ Código aprobado")
                return self.estado["final"]

            contexto = f"Refactorizar según: {decision}"

        return "⚠️ No se logró aprobación final."


# -------------------------------
# MAIN CLI
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Colmena Vertex - Generador Autónomo")
    parser.add_argument("tarea", type=str, help="Descripción del proyecto a generar")

    args = parser.parse_args()

    colmena = AgenteMaestro(max_ciclos=2)
    resultado = colmena.ejecutar(args.tarea)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    archivo_py = f"solucion_vertex_{timestamp}.py"
    archivo_pdf = f"reporte_vertex_{timestamp}.pdf"

    ruta_py = colmena.guardar_codigo(resultado, archivo_py)
    ruta_pdf = colmena.generar_pdf(resultado, archivo_pdf)

    print("\n🏆 RESULTADO FINAL")
    print("=" * 50)
    print(resultado)
    print("\n📁 Archivo Python:", ruta_py)
    print("📄 Archivo PDF:", ruta_pdf)


if __name__ == "__main__":
    main()