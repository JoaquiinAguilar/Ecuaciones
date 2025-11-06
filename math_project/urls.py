from django.contrib import admin
from django.urls import path, include  # ¡Asegúrate de importar 'include'!

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- Añadir esta línea ---
    # Esto le dice a Django: "Para cualquier URL que comience con 'solver/',
    # envía la solicitud a los archivos 'urls.py' de la app 'math_solver'".
    path("solver/", include("math_solver.urls")),
]