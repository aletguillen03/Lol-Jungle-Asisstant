# LoL Jungle Assistant

Una herramienta web para asistir a junglers de League of Legends en tiempo real, proporcionando análisis de IA, seguimiento de objetivos y sugerencias estratégicas.

## 🎯 Características

- **Dashboard Personalizado**: Estadísticas y métricas de rendimiento
- **Seguimiento en Tiempo Real**: Monitoreo de partidas activas
- **Timers de Jungla**: Seguimiento automático de objetivos (dragones, barón, heraldo)
- **Análisis de IA**: Sugerencias personalizadas usando Claude API
- **Integración con Riot API**: Datos en tiempo real de League of Legends
- **Historial de Partidas**: Análisis detallado de partidas pasadas

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos (desarrollo)
- **Pydantic** - Validación de datos
- **httpx** - Cliente HTTP asíncrono

### Frontend
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Material-UI (MUI)** - Componentes de UI
- **React Query** - Gestión de estado del servidor
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP

### APIs Externas
- **Riot Games API** - Datos de League of Legends
- **Claude API** - Análisis de IA

## 📁 Estructura del Proyecto

```
lol-jungle-assistant/
├── backend/                 # API Server (FastAPI)
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/           # Configuración
│   │   ├── models/         # Modelos de base de datos
│   │   ├── schemas/        # Esquemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── utils/          # Utilidades
│   ├── tests/              # Tests del backend
│   ├── main.py             # Punto de entrada
│   └── requirements.txt    # Dependencias Python
├── frontend/               # React App
│   ├── public/             # Archivos estáticos
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # Servicios API
│   │   └── types/          # Tipos TypeScript
│   ├── package.json        # Dependencias Node.js
│   └── tsconfig.json       # Configuración TypeScript
├── config/                 # Configuraciones
├── docs/                   # Documentación
└── README.md
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- npm o yarn
- Cuenta de desarrollador de Riot Games
- API Key de Claude (Anthropic)

### Backend Setup

1. **Navegar al directorio del backend**:
   ```bash
   cd backend
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   cp .env .env
   ```
   
   Editar `.env` con tus API keys:
   ```env
   RIOT_API_KEY=tu_riot_api_key
   CLAUDE_API_KEY=tu_claude_api_key
   ```

5. **Ejecutar el servidor**:
   ```bash
   python main.py
   ```

   El servidor estará disponible en `http://localhost:8000`

### Frontend Setup

1. **Navegar al directorio del frontend**:
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Ejecutar la aplicación**:
   ```bash
   npm start
   ```

   La aplicación estará disponible en `http://localhost:3000`

## 📖 Uso

### 1. Configuración Inicial
- Accede a la aplicación en `http://localhost:3000`
- Ve a la sección "Perfil" para configurar tu cuenta de Riot Games
- Ingresa tu Riot ID y tag line

### 2. Dashboard
- Visualiza tus estadísticas generales
- Revisa tu winrate, rango actual y KDA promedio
- Consulta sugerencias de IA personalizadas

### 3. Seguimiento de Partida
- Inicia una nueva sesión de partida
- Usa los timers automáticos para objetivos
- Recibe sugerencias en tiempo real

### 4. Análisis Post-Partida
- Revisa el análisis detallado de tu rendimiento
- Consulta recomendaciones de mejora
- Guarda notas personales

## 🔧 Desarrollo

### Comandos Útiles

**Backend**:
```bash
# Ejecutar tests
pytest

# Generar migración de base de datos
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Ejecutar con recarga automática
uvicorn main:app --reload
```

**Frontend**:
```bash
# Ejecutar tests
npm test

# Build para producción
npm run build

# Análisis del bundle
npm run analyze