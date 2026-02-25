import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv # Nueva importación
# Importamos lo que ya construimos
from example7 import AgenteMaestro, pensar 

# --- CARGA DE CONFIGURACIÓN SEGURA ---
load_dotenv() # Carga las variables del archivo .env

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def enviar_reporte(destinatario, codigo_generado):
    """Módulo de despacho final de Vertex Coders con variables de entorno."""
    # Validación de carga de variables
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return "❌ Error: Faltan credenciales en el archivo .env"

    print("✉️  Sombrero Comunicador redactando reporte final...")
    
    # El Agente Comunicador le da el toque humano
    sombrero_comunicador = {
        "rol": "Eres el Agente de Éxito del Cliente en Vertex Coders LLC.",
        "instruccion": "Redacta un mensaje profesional y entusiasta. Informa que el sistema 'Nemesis IA' ha finalizado la auditoría y el código está listo."
    }
    
    cuerpo_ai = pensar(sombrero_comunicador, "Tarea completada con éxito.")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = destinatario
    msg['Subject'] = "🚀 Entrega de Desarrollo - Vertex Services"
    
    contenido = f"{cuerpo_ai}\n\n" + "="*30 + "\nCÓDIGO ENTREGADO:\n" + "="*30 + f"\n\n{codigo_generado}"
    msg.attach(MIMEText(contenido, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return f"✅ Reporte enviado exitosamente a {destinatario}"
    except Exception as e:
        return f"❌ Error en el despacho: {e}"

# --- FLUJO COMPLETO ---
if __name__ == "__main__":
    agente_maestro = AgenteMaestro(max_ciclos=1)
    tarea = "Crear un script en Python para monitorear el uso de CPU y enviar una alerta si supera el 80%."
    resultado = agente_maestro.ejecutar(tarea)
    
    print("\n📧 Iniciando proceso de notificación...")
    status = enviar_reporte("cliente_interesado@gmail.com", resultado)
    print(status)