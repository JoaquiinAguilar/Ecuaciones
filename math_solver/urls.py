from django.urls import path
from . import views  # Importa las vistas de la aplicación actual

# Este es el 'app_name', permite a Django diferenciar
# las rutas si tuviéramos múltiples apps.
app_name = 'math_solver'

urlpatterns = [
    # URL: /solver/
    # Esta es la ruta raíz de nuestra aplicación.
    # Conecta la URL vacía ('' dentro de la app) a la función 'main_solver_view'
    # que está en 'views.py'.
    # El 'name' nos permite referirnos a esta ruta fácilmente en los templates
    # (como hicimos en index.html con {% url 'main_solver_view' %}).
    path('', views.main_solver_view, name='main_solver_view'),
]