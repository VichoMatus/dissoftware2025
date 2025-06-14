# 🎬 CineMaster - Sistema de Gestión de Cine

Sistema completo de gestión de cine desarrollado en Python con arquitectura MVC, API REST y principios SOLID.

## 📋 Características

### 🖥️ Aplicación de Escritorio
- **Interfaz gráfica moderna** con CustomTkinter
- **Sistema de autenticación** para clientes, empleados y administradores
- **Gestión de cartelera** y horarios de películas
- **Sistema de reservas** con selección de asientos
- **Procesamiento de pagos** y generación de boletas PDF
- **Perfiles de usuario** con historial de reservas

### 🚀 API REST
- **FastAPI** con documentación automática (Swagger UI)
- **Arquitectura en capas** siguiendo principios SOLID
- **Autenticación JWT**
- **Endpoints RESTful** para todas las operaciones
- **Validación de datos** con Pydantic

### 🏗️ Patrones de Diseño Implementados
- **MVC (Modelo-Vista-Controlador)**
- **Observer Pattern** - Notificaciones por email
- **Command Pattern** - Procesamiento de comandos
- **Facade Pattern** - Gestión de reservas
- **Builder Pattern** - Generación de boletas
- **Proxy Pattern** - Control de acceso a asientos

## 🛠️ Tecnologías Utilizadas

- **Python 3.12+**
- **CustomTkinter** - Interfaz gráfica moderna
- **FastAPI** - API REST de alto rendimiento
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos ligera
- **Pydantic** - Validación de datos
- **ReportLab** - Generación de PDFs
- **Pillow** - Procesamiento de imágenes

## 📁 Estructura del Proyecto

```
cinemaster/
├── src/
│   ├── main.py                 # Punto de entrada principal
│   ├── api/                    # API REST (FastAPI)
│   │   ├── main.py
│   │   ├── routers/           # Endpoints
│   │   ├── schemas/           # Modelos Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   ├── dependencies/      # Inyección de dependencias
│   │   └── config/           # Configuración
│   ├── controllers/           # Controladores MVC
│   ├── models/               # Modelos de datos
│   ├── views/                # Interfaces gráficas
│   ├── services/             # Servicios de negocio
│   ├── commands/             # Command Pattern
│   ├── builders/             # Builder Pattern
│   └── utils/                # Utilidades
├── database/                 # Scripts de BD
├── test/                     # Pruebas
├── requirements.txt          # Dependencias
└── README.md                # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd cinemaster
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# .venv\Scripts\activate   # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
La base de datos SQLite se crea automáticamente al ejecutar la aplicación por primera vez.

## 🏃‍♂️ Ejecución

### Ejecutar la aplicación completa (GUI + API)
```bash
cd cinemaster/src
python main.py
```

Esto iniciará:
- **Aplicación de escritorio** en la ventana principal
- **API REST** en `http://127.0.0.1:8000`
- **Documentación API** en `http://127.0.0.1:8000/docs`

### Solo API (sin GUI)
```bash
cd cinemaster/src/api
python main.py
```

## 📖 Uso del Sistema

### 👥 Tipos de Usuario

1. **Cliente**
   - Registrarse/Iniciar sesión
   - Ver cartelera de películas
   - Reservar asientos
   - Procesar pagos
   - Ver historial de reservas

2. **Empleado**
   - Gestionar reservas de clientes
   - Procesar pagos en taquilla
   - Ver estadísticas básicas

3. **Administrador**
   - Gestión completa de películas
   - Administrar horarios y salas
   - Ver reportes y estadísticas
   - Gestionar usuarios del sistema

### 🎟️ Proceso de Reserva

1. **Seleccionar película** desde la cartelera
2. **Elegir horario** disponible
3. **Seleccionar asientos** en la sala
4. **Procesar pago** (efectivo o tarjeta)
5. **Generar boleta** en PDF automáticamente
6. **Recibir confirmación** por email (opcional)

## 🔧 API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario

### Películas
- `GET /api/v1/peliculas` - Listar películas
- `GET /api/v1/peliculas/{id}` - Obtener película específica

### Reservas
- `POST /api/v1/reservas` - Crear reserva
- `GET /api/v1/reservas` - Listar reservas del usuario

### Clientes
- `GET /api/v1/clientes` - Listar clientes (admin)
- `GET /api/v1/clientes/{id}` - Obtener cliente específico

## 🧪 Pruebas

```bash
cd cinemaster
python -m pytest test/
```

## 📝 Principios SOLID Aplicados

- **S** - Single Responsibility: Cada clase tiene una responsabilidad específica
- **O** - Open/Closed: Extensible sin modificar código existente
- **L** - Liskov Substitution: Subclases intercambiables
- **I** - Interface Segregation: Interfaces específicas y pequeñas
- **D** - Dependency Inversion: Dependencias inyectadas, no hardcodeadas

## 🏛️ Arquitectura

### Patrón MVC
- **Model**: `models/` - Entidades y lógica de datos
- **View**: `views/` - Interfaces gráficas
- **Controller**: `controllers/` - Lógica de control y navegación

### API en Capas
- **Presentation Layer**: `routers/` - Endpoints HTTP
- **Business Logic Layer**: `services/` - Lógica de negocio
- **Data Access Layer**: `models/` - Acceso a datos

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado como proyecto académico para el curso de Diseño de Software.

## 📞 Soporte

Para reportar bugs o solicitar features, por favor abrir un issue en el repositorio.

---

⭐ Si te gusta el proyecto, ¡dale una estrella en GitHub!
