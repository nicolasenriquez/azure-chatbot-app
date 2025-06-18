# 🤖 Azure AI Chatbot - Aplicación Fullstack

Una aplicación completa de chatbot impulsada por Azure AI con frontend React moderno y backend FastAPI profesional.

## 🌟 Características

- **Frontend React**: Interfaz moderna con tema oscuro y componentes reutilizables
- **Backend FastAPI**: API robusta con integración Azure AI
- **Azure OpenAI**: Conversaciones inteligentes con GPT-4o
- **Azure AI Search**: Base de conocimiento para respuestas contextual
- **Deployment Automatizado**: GitHub Actions + Azure App Services
- **Responsive Design**: Optimizado para desktop, tablet y móvil

## 🏗️ Arquitectura

```
azure-chatbot-app/
├── frontend/          # Aplicación React + TypeScript
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── backend/           # API FastAPI + Python
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── .github/workflows/ # GitHub Actions
├── docs/             # Documentación
└── README.md
```

## 🚀 Quick Start

### Prerrequisitos

- Node.js 18+
- Python 3.11+
- Cuenta de Azure con acceso a OpenAI
- Git

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/azure-chatbot-app.git
cd azure-chatbot-app
```

### 2. Configurar Backend

```bash
cd backend
pip install -r requirements.txt

# Crear archivo .env
cat > .env << EOF
AZURE_OPENAI_API_KEY=tu_clave_openai
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_SEARCH_ENDPOINT=https://tu-servicio.search.windows.net
AZURE_SEARCH_API_KEY=tu_clave_search
EOF

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Configurar Frontend

```bash
cd frontend
npm install

# Crear archivo .env.local
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Ejecutar aplicación
npm run dev
```

### 4. Abrir Aplicación

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/docs`

## 📁 Estructura del Proyecto

### Frontend (React + TypeScript)

```
frontend/
├── src/
│   ├── components/       # Componentes UI
│   │   ├── ui/          # Componentes base (shadcn/ui)
│   │   └── chat/        # Componentes específicos del chat
│   ├── hooks/           # Custom hooks React
│   ├── lib/             # Utilidades y API
│   ├── pages/           # Páginas de la aplicación
│   └── index.css        # Estilos globales
├── package.json         # Dependencias y scripts
├── vite.config.ts       # Configuración Vite
└── tailwind.config.ts   # Configuración Tailwind
```

### Backend (FastAPI + Python)

```
backend/
├── routers/             # Endpoints API
│   ├── chat.py         # Rutas del chat
│   ├── conversations.py # Gestión conversaciones
│   └── health.py       # Health checks
├── services/           # Lógica de negocio
│   ├── azure_ai.py     # Integración Azure AI
│   ├── chatbot.py      # Servicio chatbot
│   └── storage.py      # Gestión datos
├── schemas/            # Modelos Pydantic
├── config/             # Configuración
├── utils/              # Utilidades
└── main.py             # Punto entrada
```

## 🔧 Variables de Entorno

### Backend (.env)

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=tu_clave_aqui
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://tu-servicio.search.windows.net
AZURE_SEARCH_API_KEY=tu_clave_aqui
AZURE_SEARCH_INDEX_NAME=knowledge-base

# Aplicación
ENVIRONMENT=development
PORT=8000
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```env
VITE_API_URL=http://localhost:8000
```

## 🚀 Deployment en Azure

### 1. Preparación Rápida

```bash
# Crear recursos Azure
az group create --name rg-chatbot --location "East US"

# Backend
az webapp create \
  --name chatbot-backend-[TU-NOMBRE] \
  --resource-group rg-chatbot \
  --plan plan-chatbot \
  --runtime "PYTHON|3.11"

# Frontend  
az webapp create \
  --name chatbot-frontend-[TU-NOMBRE] \
  --resource-group rg-chatbot \
  --plan plan-chatbot \
  --runtime "NODE|18-lts"
```

### 2. Configurar GitHub Secrets

En tu repositorio GitHub:
- `AZURE_CREDENTIALS`: JSON del service principal
- `AZURE_WEBAPP_NAME_BACKEND`: Nombre del app backend
- `AZURE_WEBAPP_NAME_FRONTEND`: Nombre del app frontend

### 3. Push y Deploy

```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

GitHub Actions desplegará automáticamente tu aplicación.

## 📖 Documentación Completa

- **[Guía de Deployment](docs/DEPLOYMENT_GUIDE.md)**: Configuración completa de Azure
- **[Guía de Frontend](docs/FRONTEND_GUIDE.md)**: Desarrollo con React
- **[Guía de Backend](docs/BACKEND_GUIDE.md)**: Desarrollo con FastAPI

## 🔌 API Endpoints

### Chat
- `POST /api/chat`: Enviar mensaje
- `GET /api/conversations`: Listar conversaciones
- `GET /api/conversations/{id}/messages`: Mensajes de conversación

### Health
- `GET /api/health`: Estado del servidor

### Ejemplos

```bash
# Enviar mensaje
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿cómo estás?"}'

# Listar conversaciones
curl http://localhost:8000/api/conversations
```

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React 18**: Framework principal
- **TypeScript**: Tipado estático
- **Vite**: Build tool rápido
- **Tailwind CSS**: Framework de estilos
- **shadcn/ui**: Componentes accesibles
- **TanStack Query**: Gestión estado servidor

### Backend
- **FastAPI**: Framework web moderno
- **Python 3.11**: Lenguaje backend
- **Pydantic**: Validación datos
- **Azure OpenAI**: IA conversacional
- **Azure AI Search**: Base conocimiento

### DevOps
- **GitHub Actions**: CI/CD automatizado
- **Azure App Services**: Hosting cloud
- **Docker**: Containerización

## 🐛 Solución de Problemas

### Error "Missing environment variables"
```bash
# Verificar variables backend
cat backend/.env

# Verificar variables frontend  
cat frontend/.env.local
```

### Frontend no conecta con Backend
```bash
# Verificar CORS en backend
# Verificar VITE_API_URL en frontend
```

### Azure OpenAI no responde
```bash
# Verificar credenciales
az cognitiveservices account keys list --name tu-recurso --resource-group tu-rg
```

## 📝 Scripts Útiles

### Desarrollo
```bash
# Instalar todo
npm run install:all

# Ejecutar todo
npm run dev:all

# Build producción
npm run build:all
```

### Deployment
```bash
# Deploy manual backend
az webapp deploy --name tu-backend --src-path backend/

# Deploy manual frontend
az webapp deploy --name tu-frontend --src-path frontend/dist/
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la [documentación](docs/)
2. Busca en [Issues](https://github.com/tu-usuario/azure-chatbot-app/issues)
3. Crea un nuevo issue con detalles

## 🎯 Roadmap

- [ ] Autenticación de usuarios
- [ ] Base de datos PostgreSQL
- [ ] Análisis de conversaciones
- [ ] API de administración
- [ ] Modo multi-idioma
- [ ] Integración con Teams/Slack

---

**¡Tu chatbot con Azure AI está listo para producción!**

Para empezar rápidamente, sigue la [Guía de Deployment](docs/DEPLOYMENT_GUIDE.md) paso a paso.
