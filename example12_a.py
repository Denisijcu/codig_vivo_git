from openai import OpenAI
import logging

# Configuración de logs para observabilidad Enterprise
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

class Orquestador:
    def __init__(self, memoria, seguridad, auditor):
        self.memoria = memoria
        self.seguridad = seguridad
        self.auditor = auditor
        self.max_tokens_contexto = 6000 # Límite para qwen2-7b 

    def gestionar_ventana_contexto(self, contexto):
        """ Hardening: Recorta el contexto si excede el límite de la ventana """
        if len(str(contexto)) > self.max_tokens_contexto:
            logging.warning("⚠️ Contexto excedido. Aplicando recorte (Trimming).")
            return contexto[-self.max_tokens_contexto:]
        return contexto

    def procesar(self, mensaje):
        # 1. Recuperación y limpieza de contexto (RAG) [cite: 8732]
        contexto_crudo = self.memoria.recuperar(mensaje)
        contexto_limpio = self.gestionar_ventana_contexto(contexto_crudo)
        
        # 2. Validación de Seguridad (Protocolo Némesis) [cite: 9682]
        if not self.seguridad.validar(mensaje):
            logging.error(f"❌ Intento de inyección detectado en: {mensaje}")
            return "Error: Petición bloqueada por políticas de seguridad."

        # 3. Ejecución del Agente
        respuesta = self._ejecutar_agente(mensaje, contexto_limpio)
        
        # 4. Auditoría y Registro [cite: 9110]
        self.auditor.registrar(mensaje, respuesta)
        return respuesta

    def _ejecutar_agente(self, mensaje, contexto):
        try:
            # Corrección de sintaxis y versionado de modelo [cite: 8462]
            response = client.chat.completions.create(
                model="qwen2-7b-instruct", 
                messages=[
                    {"role": "system", "content": f"Contexto de Memoria Soberana: {contexto}"},
                    {"role": "user", "content": mensaje}
                ],
                temperature=0.2 # Rigor técnico solicitado [cite: 9049]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"❌ Error en inferencia: {e}")
            return "Lo siento, el cerebro local no responde."

# Nota: Este código ahora cumple con la gestión de errores y el logging
# que exige un entorno de producción real para 2026.

# --- 3. ENTRADA PRINCIPAL (MAIN) ---
if __name__ == "__main__":
    # 1. Simulación de los Componentes (Mocks para la prueba)
    class MemoriaMock:
        def recuperar(self, msg): 
            return "DATO_TECNICO: El servidor de Vertex usa el puerto 8080."

    class SeguridadMock:
        def validar(self, msg): 
            # Bloquea si detecta palabras prohibidas (Protocolo Némesis)
            prohibido = ["DROP", "DELETE", "GRANT"]
            return not any(p in msg.upper() for p in prohibido)

    class AuditorMock:
        def registrar(self, msg, res): 
            logging.info(f"📝 Auditoría: Mensaje='{msg}' | Respuesta Generada.")

    # 2. Instanciación del Sistema Soberano
    memoria = MemoriaMock()
    seguridad = SeguridadMock()
    auditor = AuditorMock()
    
    orquestador = Orquestador(memoria, seguridad, auditor)

    # 3. Casos de Prueba
    print("\n🚀 --- TEST DE SISTEMA VERTEX ---")
    
    # Prueba 1: Petición Legítima
    print("\n👤 Usuario: ¿En qué puerto corre el sistema?")
    respuesta1 = orquestador.procesar("¿En qué puerto corre el sistema?")
    print(f"🤖 Agente: {respuesta1}")

    # Prueba 2: Intento de Inyección (Hardening)
    print("\n👤 Usuario: DROP TABLE users;")
    respuesta2 = orquestador.procesar("DROP TABLE users;")
    print(f"🤖 Agente: {respuesta2}")


