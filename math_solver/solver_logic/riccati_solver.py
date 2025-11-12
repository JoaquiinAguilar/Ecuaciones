from sympy import Eq, dsolve, latex
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_riccati(P_str: str, Q_str: str, R_str: str) -> dict:
    """
    Resuelve una Ecuación de Riccati y proporciona los pasos.
    """
    
    # 1. Parsear y Validar
    p_expr = parse_safe(P_str)
    if p_expr is None: return {'error': f"P(x) = '{P_str}' no es válida."}

    q_expr = parse_safe(Q_str)
    if q_expr is None: return {'error': f"Q(x) = '{Q_str}' no es válida."}

    r_expr = parse_safe(R_str)
    if r_expr is None: return {'error': f"R(x) = '{R_str}' no es válida."}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir la Ecuación Original
        ecuacion = Eq(y.diff(x), (p_expr * y**2) + (q_expr * y) + r_expr)
        steps.append(f"1. La ecuación de Riccati es: \( {latex(ecuacion)} \)")
        steps.append(f"   - Con \( P(x) = {latex(p_expr)} \), \( Q(x) = {latex(q_expr)} \) y \( R(x) = {latex(r_expr)} \).")

        # 3. Explicación del Método de Solución
        steps.append("2. Las ecuaciones de Riccati son no lineales y, en general, no tienen una solución elemental. Suelen resolverse si se conoce una <strong>solución particular</strong> (\(y_p\)).")
        steps.append("3. Con una solución particular, se usa la sustitución \( y = y_p + u \) para transformar la ecuación de Riccati en una ecuación de Bernoulli, que luego se puede resolver.")
        steps.append("4. SymPy intenta encontrar una solución particular y realizar esta transformación de forma automática.")

        # 4. Resolver y Formatear
        solucion = dsolve(ecuacion, y)
        
        if not solucion:
            return {'error': "SymPy no pudo encontrar una solución para esta ecuación de Riccati."}

        solucion_latex = format_latex(solucion)
        steps.append(f"5. La solución encontrada por SymPy es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}