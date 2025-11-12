from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# --- 1. Importar TODOS los solvers de nuestra lógica ---
from .solver_logic.quadratic_solver import solve_quadratic
from .solver_logic.bernoulli_solver import solve_bernoulli
from .solver_logic.cauchy_euler_solver import solve_cauchy_euler
from .solver_logic.clairaut_solver import solve_clairaut
from .solver_logic.riccati_solver import solve_riccati
from .solver_logic.second_order_solver import solve_second_order_homogeneous, solve_second_order_nonhomogeneous

@require_http_methods(["GET", "POST"])
def main_solver_view(request):
    """
    Controla la página principal, maneja las solicitudes GET (mostrar página)
    y POST (procesar formulario).
    
    Esta vista ahora maneja los 5 tipos de solvers usando
    nombres de input únicos para evitar conflictos.
    """
    
    # Contexto inicial
    # 'last_solver' se usa para decirle al HTML qué pestaña mostrar.
    # Por defecto (en GET) es 'quadratic'.
    context = {'last_solver': 'quadratic'}

    if request.method == 'POST':
        try:
            # Identificar qué formulario se envió
            solver_type = request.POST.get('solver_type')
            
            # ¡IMPORTANTE! Devolvemos el 'solver_type' al contexto
            # para que la página recargue la pestaña correcta.
            context['last_solver'] = solver_type

            # --- 2. Lógica de enrutamiento basada en solver_type ---
            
            if solver_type == 'quadratic':
                # --- CORREGIDO: Nombres únicos ---
                a_str = request.POST.get('quad_a_val', '0')
                b_str = request.POST.get('quad_b_val', '0')
                c_str = request.POST.get('quad_c_val', '0')
                # Llamar a la lógica del solver cuadrático
                context.update(solve_quadratic(a_str, b_str, c_str))

            elif solver_type == 'bernoulli':
                # --- CORREGIDO: Nombres únicos ---
                P_str = request.POST.get('bernoulli_p_function', '')
                Q_str = request.POST.get('bernoulli_q_function', '')
                n_str = request.POST.get('bernoulli_n_value', '')
                # Llamar a la lógica del solver de Bernoulli
                context.update(solve_bernoulli(P_str, Q_str, n_str))
            
            # --- CORREGIDO: 'cauchy_euler' a 'cauchy' para coincidir con el HTML ---
            elif solver_type == 'cauchy':
                # --- CORREGIDO: Nombres únicos ---
                a_str = request.POST.get('cauchy_a_val', '0')
                b_str = request.POST.get('cauchy_b_val', '0')
                c_str = request.POST.get('cauchy_c_val', '0')
                R_str = request.POST.get('cauchy_r_function', '0')
                # Llamar a la lógica del solver de Cauchy-Euler
                context.update(solve_cauchy_euler(a_str, b_str, c_str, R_str))

            elif solver_type == 'clairaut':
                # --- CORREGIDO: Nombres únicos ---
                f_p_str = request.POST.get('clairaut_f_p_function', '')
                # Llamar a la lógica del solver de Clairaut
                context.update(solve_clairaut(f_p_str))
                
            elif solver_type == 'riccati':
                # --- CORREGIDO: Nombres únicos ---
                P_str = request.POST.get('riccati_p_function', '')
                Q_str = request.POST.get('riccati_q_function', '')
                R_str = request.POST.get('riccati_r_function', '')
                # Llamar a la lógica del solver de Riccati
                context.update(solve_riccati(P_str, Q_str, R_str))
                
            elif solver_type == 'second_order_homogeneous':
                # --- Solver de segundo orden homogéneo ---
                a_str = request.POST.get('second_a_val', '0')
                b_str = request.POST.get('second_b_val', '0')
                c_str = request.POST.get('second_c_val', '0')
                # Llamar a la lógica del solver de segundo orden homogéneo
                context.update(solve_second_order_homogeneous(a_str, b_str, c_str))
                
            elif solver_type == 'second_order_nonhomogeneous':
                # --- Solver de segundo orden no homogéneo ---
                a_str = request.POST.get('second_a_val', '0')
                b_str = request.POST.get('second_b_val', '0')
                c_str = request.POST.get('second_c_val', '0')
                g_str = request.POST.get('second_g_function', '0')
                # Llamar a la lógica del solver de segundo orden no homogéneo
                context.update(solve_second_order_nonhomogeneous(a_str, b_str, c_str, g_str))

            else:
                context = {'error': f'Tipo de solver desconocido: "{solver_type}"'}

        except Exception as e:
            # Captura de error general
            context = {'error': f'Ha ocurrido un error inesperado en la vista: {e}'}

    # 3. Renderizar la página
    # Si es GET, context es {'last_solver': 'quadratic'}.
    # Si es POST, context contiene la 'solucion' o 'error' Y 'last_solver'.
    return render(request, 'math_solver/index.html', {'context': context})