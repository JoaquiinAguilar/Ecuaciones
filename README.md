# Math Solver Pro - Ecuaciones Diferenciales

🧮 **Sistema avanzado para resolver ecuaciones diferenciales y matemáticas**

Un proyecto web completo para resolver diferentes tipos de ecuaciones matemáticas con interfaz moderna y persistencia de datos.

## 🚀 Características Principales

### 📊 Tipos de Ecuaciones Soportadas
- **Ecuaciones Cuadráticas**: `ax² + bx + c = 0`
- **Ecuaciones de Bernoulli**: `y' + P(x)y = Q(x)yⁿ`
- **Ecuaciones de Cauchy-Euler**: `ax²y'' + bxy' + cy = R(x)`
- **Ecuaciones de Clairaut**: `y = xy' + f(y')`
- **Ecuaciones de Riccati**: `y' = P(x)y² + Q(x)y + R(x)`
- **Ecuaciones de Segundo Orden**: `ay'' + by' + cy = g(x)`

### 🎛️ Paleta de Funciones Matemáticas
- **Funciones Trigonométricas**: sin, cos, tan, cot, sec, csc y sus inversas
- **Funciones Exponenciales y Logarítmicas**: exp, log, ln
- **Potencias y Raíces**: √x, x², x³, valor absoluto
- **Funciones Especiales**: Hiperbólicas, Airy, Bessel
- **Constantes Matemáticas**: π, e, i, ∞
- **Polinomios Comunes**: Formatos predefinidos

### 💡 Características Avanzadas
- ✅ **Persistencia de Datos**: Los datos se guardan automáticamente
- ✅ **AJAX Integration**: Respuestas instantáneas sin recargar página
- ✅ **MathJax Rendering**: Formato matemático profesional
- ✅ **Responsive Design**: Funciona en todos los dispositivos
- ✅ **Keyboard Shortcuts**: Atajos para productividad
- ✅ **Solution History**: Historial de soluciones por tipo
- ✅ **Error Handling**: Mensajes de error detallados

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.x**: Framework web principal
- **SymPy**: Computación simbólica y matemática
- **Python 3.x**: Lenguaje de programación

### Frontend
- **Tailwind CSS**: Framework CSS moderno
- **JavaScript ES6+**: Lógica interactiva del cliente
- **MathJax 3**: Renderizado de expresiones matemáticas
- **LocalStorage**: Persistencia de datos en el navegador

### Arquitectura
- **MVC Pattern**: Separación clara de responsabilidades
- **AJAX Requests**: Comunicación asíncrona
- **Component-Based**: Componentes reutilizables

## 📁 Estructura del Proyecto

```
math_project/
├── math_solver/                 # Aplicación principal
│   ├── solver_logic/            # Lógica de solvers
│   │   ├── base_solver.py      # Clase base
│   │   ├── quadratic_solver.py # Ecuaciones cuadráticas
│   │   ├── bernoulli_solver.py # Ecuaciones de Bernoulli
│   │   ├── cauchy_euler_solver.py # Ecuaciones de Cauchy-Euler
│   │   ├── clairaut_solver.py  # Ecuaciones de Clairaut
│   │   ├── riccati_solver.py   # Ecuaciones de Riccati
│   │   └── second_order_solver.py # Ecuaciones de segundo orden
│   ├── templates/math_solver/   # Plantillas HTML
│   ├── static/math_solver/      # Archivos estáticos
│   │   ├── css/style.css      # Estilos personalizados
│   │   └── js/main.js        # Lógica JavaScript
│   ├── views.py               # Vistas Django
│   ├── urls.py                # URLs de la aplicación
│   └── models.py              # Modelos de datos
├── math_project/               # Configuración del proyecto
│   ├── settings.py            # Configuración Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # WSGI configuration
├── manage.py                  # Script de gestión Django
├── requirements.txt           # Dependencias Python
└── README.md                # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd math_project
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones de Django**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Iniciar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

6. **Acceder a la aplicación**
   - URL principal: `http://127.0.0.1:8000/solver/`
   - Página de ayuda: `http://127.0.0.1:8000/solver/help/`

## 📖 Uso de la Aplicación

### Uso Básico
1. **Seleccionar tipo de ecuación** en el panel izquierdo
2. **Ingresar parámetros** en los campos correspondientes
3. **Usar paleta de funciones** para insertar expresiones matemáticas
4. **Presionar "Resolver Ecuación"** para obtener solución
5. **Ver resultados detallados** con pasos y verificación

### Atajos de Teclado
- `Ctrl+Space`: Mostrar ayuda de atajos
- `Tab`: Navegar entre campos
- `Enter`: Resolver ecuación
- `Escape`: Cerrar ventanas de ayuda

### Paleta de Funciones
- **Click en campo**: Activar campo de entrada
- **Click en función**: Insertar en posición del cursor
- **Hover**: Ver descripción de la función

## 🧮 Ejemplos de Uso

### Ecuación Cuadrática
```
Parámetros: a=1, b=-5, c=6
Ecuación: x² - 5x + 6 = 0
Solución: x₁=3, x₂=2
```

### Ecuación de Bernoulli
```
Parámetros: P(x)=2/x, Q(x)=x, n=2
Ecuación: y' + (2/x)y = xy²
Solución: y = 1/(Cx² - x³/3)
```

### Ecuación de Riccati
```
Parámetros: P(x)=1, Q(x)=-x, R(x)=1
Ecuación: y' = y² - xy + 1
Solución: y = x + (e^(-x²))/(C - ∫e^(-x²)dx)
```

## 🔧 Desarrollo y Contribución

### Arquitectura de Solvers
Cada solver hereda de `BaseSolver` e implementa:
- `solve()`: Método principal de resolución
- `format_solution()`: Formateo de resultados
- `validate_input()`: Validación de parámetros

### Extensión del Sistema
Para agregar nuevos tipos de ecuaciones:
1. Crear nueva clase en `solver_logic/`
2. Heredar de `BaseSolver`
3. Implementar métodos requeridos
4. Agregar rutas en `views.py`
5. Crear plantilla HTML correspondiente

### Estándares de Código
- **Python**: PEP 8 compliance
- **JavaScript**: ES6+ standards
- **CSS**: Tailwind CSS conventions
- **HTML**: Semantic HTML5

## 🐛 Solución de Problemas

### Problemas Comunes
1. **Error de importación**: Verificar instalación de SymPy
2. **MathJax no renderiza**: Revisar conexión a internet
3. **Datos no persisten**: Verificar localStorage habilitado
4. **Funciones no reconocidas**: Usar sintaxis SymPy correcta

### Depuración
- **Consola del navegador**: Ver errores JavaScript
- **Logs de Django**: `python manage.py runserver --verbosity=2`
- **Modo desarrollo**: `DEBUG=True` en settings.py

## 📄 Licencia

Este proyecto está desarrollado para fines educativos y de investigación en el área de matemáticas computacionales.

## 👥 Autores

- **Desarrollador Principal**: [Tu Nombre]
- **Institución**: Ingeniería en Sistemas Computacionales 9no semestre

## 🙏 Agradecimientos

- **SymPy Team**: Por la excelente librería de computación simbólica
- **Django Foundation**: Por el framework web robusto
- **MathJax Consortium**: Por el renderizado matemático de calidad

## 📞 Contacto y Soporte

- **Issues y Bugs**: Reportar en el repositorio del proyecto
- **Sugerencias**: Bienvenidas en el sistema de issues
- **Documentación**: Ver página de ayuda integrada

---

**Nota**: Este proyecto es parte del coursework de Ingeniería en Sistemas Computacionales y está diseñado para facilitar el aprendizaje y resolución de ecuaciones diferenciales.