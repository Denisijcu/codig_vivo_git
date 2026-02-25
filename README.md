

# 🚀 Código Vivo: La Colmena Sintética de Vertex Coders

Bienvenido al repositorio oficial de **"Código Vivo"**. Este proyecto documenta la creación de una infraestructura de agentes autónomos capaces de razonar, escribir código y autoprotegerse utilizando inteligencia artificial local.

## 🧠 Sobre el Proyecto

Este sistema implementa el **Protocolo de los 6 Sombreros de Pensamiento** aplicado a la ingeniería de software, permitiendo que múltiples agentes especializados (Blanco, Negro, Verde, Rojo, Amarillo y Azul) colaboren para entregar soluciones de alta calidad sin depender de nubes externas.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python.
* **Cerebro Local:** LM Studio (qwen2-7b-instruct) vía API.
* **Memoria de Largo Plazo:** FAISS para almacenamiento de vectores.
* **Seguridad:** Protocolo Némesis IA (Defensa activa en Windows).
* **Infraestructura:** Docker para despliegue soberano.
* **Frontend:** Flask con interfaz web para control de la colmena.

## 📂 Estructura de Ejemplos

El proyecto está dividido en capítulos prácticos que puedes ejecutar individualmente:

* **Capítulo 1-4:** Fundamentos de prompts y agentes básicos.
* **Capítulo 5:** Implementación de memoria con FAISS.
* **Capítulo 7-8:** La Colmena Maestra y sistemas de notificación.
* **Capítulo 9-10:** Blindaje con el Protocolo Némesis (Ciberseguridad).
* **Capítulo 11:** Dockerización y despliegue profesional.

## 🚀 Instalación Rápida (Docker)

Para desplegar la colmena completa en segundos:

1. Clona el repositorio.
2. Asegúrate de tener **LM Studio** corriendo en el puerto 1234.
3. Construye la imagen:
```bash
docker build -t vertex-colmena .

```


4. Lanza el contenedor:
```bash
docker run -p 5000:5000 --name guardian_vertex vertex-colmena

```


5. Accede a `http://localhost:5000` en tu navegador.

## 🛡️ Seguridad

Este sistema incluye el **Protocolo Némesis**, diseñado para detectar intentos de inyección de prompts y ataques de fuerza bruta en tiempo real, bloqueando automáticamente las amenazas en el firewall de Windows.

---

**Desarrollado por Denis Sanchez Leyva (CEO de Vertex Coders LLC)**.
*"Transformando líneas de código en agentes con criterio."*

