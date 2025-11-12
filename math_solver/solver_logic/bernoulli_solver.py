from sympy import Eq, dsolve, Function, pde_separate_add, latex
# Importamos nuestros símbolos y funciones comunes del base_solver
from .base_solver import x, y, parse_safe, format_latex

def solve_bernoulli(P_str: str, Q_str: str, n_str: str) -> dict:
    """
    Resuelve una ecuación de Bernoulli y proporciona los pasos.
    """
    
    # 1. Parsear y Validar
    p_expr = parse_safe(P_str)
    if p_expr is None: return {'error': f"P(x) = '{P_str}' no es válido."}

    q_expr = parse_safe(Q_str)
    if q_expr is None: return {'error': f"Q(x) = '{Q_str}' no es válido."}

    n_expr = parse_safe(n_str)
    if n_expr is None: return {'error': f"n = '{n_str}' no es válido."}
    if n_expr == 1 or n_expr == 0:
        return {'error': "El método de Bernoulli no aplica para n=0 o n=1."}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir Ecuación Original
        ecuacion_original = Eq(y.diff(x) + p_expr * y, q_expr * y**n_expr)
        steps.append(f"La ecuación de Bernoulli es: \( {latex(ecuacion_original)} \)")
        steps.append(f"   - Con \( P(x) = {latex(p_expr)} \), \( Q(x) = {latex(q_expr)} \) y \( n = {latex(n_expr)} \).")

        # 3. Transformación a Lineal
        v = Function('v')(x)
        m = 1 - n_expr
        steps.append(f"Se aplica la sustitución \( v = y^{{1-n}} = y^{{{m}}} \). Esto la convierte en una EDO lineal.")
        
        # Ecuación lineal en v: v' + (1-n)P(x)v = (1-n)Q(x)
        p_lineal = m * p_expr
        q_lineal = m * q_expr
        ecuacion_lineal = Eq(v.diff(x) + p_lineal * v, q_lineal)
        steps.append(f"   - La ecuación lineal transformada para \(v(x)\) es: \( {latex(ecuacion_lineal)} \)")

        # 4. Resolver la Ecuación Lineal para v(x)
        steps.append(f"Se resuelve la ecuación lineal para \(v(x)\), usualmente con un factor integrante.")
        sol_v = dsolve(ecuacion_lineal, v)
        steps.append(f"   - La solución para \(v(x)\) es: \( {latex(sol_v)} \)")

        # 5. Sustituir de Vuelta a y(x)
        steps.append(f"Finalmente, se sustituye \( v = y^{{{m}}} \) para obtener la solución para \(y(x)\).")
        sol_y = dsolve(ecuacion_original, y)
        solucion_latex = format_latex(sol_y)
        steps.append(f"   - La solución final es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}