# 🛠️ Hackaton Backend

¡Bienvenido al repositorio del backend de nuestro proyecto de hackatón! Este README contiene las instrucciones esenciales para que puedas clonar el proyecto, configurar tu entorno de desarrollo y poner la aplicación en marcha en cuestión de minutos.

> **Tip rápido** — Si tienes algún problema con las instrucciones o detectas algún error, abre un issue o envía un pull request 😉.

---

## 📚 Tabla de contenidos
1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
   * [Crear ambiente virtual](#crear-ambiente-virtual)
3. [Variables de entorno](#variables-de-entorno)
4. [Ejecución local](#ejecución-local)
5. [Pruebas](#pruebas)
6. [Despliegue](#despliegue)
7. [Guía de contribución](#guía-de-contribución)
8. [Licencia](#licencia)

---

## 🔧 Requisitos

| Herramienta       | Versión mínima |
|-------------------|----------------|
| Python            | 3.11           |
| pip               | 23.x           |
| git               | 2.30           |
| Sistema operativo | Windows / macOS / Linux |

> **Nota:** Si usas Windows, los comandos de activación del entorno virtual cambian ligeramente. Consulta las [FAQs](#faq).

---

## 🚀 Instalación

Clona el repositorio y entra a la carpeta principal:

```bash
# HTTPS
git clone https://github.com/tu-usuario/hackatonBackend.git


# 1. Crear el entorno virtual
python3.11 -m venv hackaton_env

# 2. Activar el entorno virtual
source hackaton_env/bin/activate  # macOS o Linux
# .\hackaton_env\Scripts\activate # Windows PowerShell

# 3. Instalar dependencias
cd hackatonBackend
pip install -r requirements.txt
