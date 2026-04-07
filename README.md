# SIGA - Sistema Integral de Gestión Académica

Plataforma centralizada para la administración de inscripciones, alumnos, carreras y docentes de los institutos de formación de la provincia. Desarrollado con [Reflex](https://reflex.dev/).

---

## 🚀 Requisitos Previos

Asegurate de tener instalados:

- **Python** 3.11 o superior.
- **Git** para clonar el repositorio.

---

## 🛠 Instalación y Configuración

Sigue estos pasos para poner en marcha el entorno de desarrollo local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/benabhi/siga.git
cd siga
```

### 2. Crear y activar el entorno virtual

Se recomienda usar un entorno virtual para aislar las dependencias:

```bash
# En Windows (Powershell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

El proyecto se comunica con un backend (ej: Directus). Necesitás configurar el archivo de entorno.

- Creá un archivo llamado `.env` en la raíz del proyecto.
- Agregá las siguientes variables (completalas con los datos reales que uses en tu backend de prueba):

```env
DIRECTUS_URL="https://tu-url-de-directus.com"
DIRECTUS_ADMIN_TOKEN="tu_token_de_acceso_admin"

# (Opcional) Usuarios de prueba
TEST_USER_EMAIL="tucorreo@tuemail.com"
TEST_USER_PASSWORD="tu_password"
```

### 5. Iniciar la aplicación

Ejecutá el siguiente comando para levantar el entorno de desarrollo. Reflex se va a encargar de compilar el frontend la primera vez:

```bash
reflex run
```

La aplicación estará disponible localmente en **http://localhost:3000**.

---

## 📂 Estructura del Proyecto

- `siga/`: Carpeta principal de la aplicación.
  - `components/`: Componentes UI reutilizables (como el `logo`).
  - `layouts/`: Plantillas principales (estructura general, menús, sidebar).
  - `pages/`: Vistas de la aplicación ordenadas por roles o módulos (ej: `/secretaria`).
  - `services/`: Comunicación con APIs externas (ej: Directus).
  - `scripts/`: Scripts de uso general (ej: seeders).
  - `state.py`: Manejo del estado global de la app y lógica de autenticación.
  - `config.py`: Variables maestras o items del menú.


