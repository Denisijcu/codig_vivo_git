import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Importamos lo que ya construimos
from example7 import AgenteMaestro, pensar 

# --- CONFIGURACIÓN DE CORREO DE VERTEX SERVICES ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "" 
SENDER_PASSWORD = "" # La contraseña de aplicación de 16 letras de Google

# --- REFINAMIENTO DEL DESPACHO ---
def enviar_reporte(destinatario, codigo_generado):
    """Módulo de despacho final de Vertex Coders."""
    print("✉️  Sombrero Comunicador redactando reporte final...")
    
    # El Agente Comunicador le da el toque humano
    sombrero_comunicador = {
        "rol": "Eres el Agente de Éxito del Cliente en Vertex Coders LLC.",
        "instruccion": "Redacta un mensaje profesional y entusiasta. Informa que el sistema 'Nemesis IA' ha finalizado la auditoría y el código está listo."
    }
    
    # Limpiamos el código de posibles explicaciones para el reporte
    cuerpo_ai = pensar(sombrero_comunicador, "Tarea completada con éxito.")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = destinatario
    msg['Subject'] = "🚀 Entrega de Desarrollo - Vertex Services"
    
    # Estructura limpia del correo
    contenido = f"{cuerpo_ai}\n\n" + "="*30 + "\nCÓDIGO ENTREGADO:\n" + "="*30 + f"\n\n{codigo_generado}"
    msg.attach(MIMEText(contenido, 'plain'))

    try:
        # Uso de contexto 'with' para asegurar que la conexión se cierre sola
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return f"✅ Reporte enviado exitosamente a {destinatario}"
    except Exception as e:
        return f"❌ Error en el despacho: {e}"

# --- FLUJO COMPLETO ---
if __name__ == "__main__":
    # 1. Instanciamos la Colmena
    agente_maestro = AgenteMaestro(max_ciclos=1)
    
    # 2. Generamos el código (aquí es donde se crea la variable 'resultado')
    tarea = "Crear un script en Python para monitorear el uso de CPU y enviar una alerta si supera el 80%."
    resultado = agente_maestro.ejecutar(tarea) # <--- AQUÍ SE DEFINE
    
    # 3. Enviamos el resultado
    print("\n📧 Iniciando proceso de notificación...")
    status = enviar_reporte("denisijcu266@gmail.com", resultado)
    print(status)