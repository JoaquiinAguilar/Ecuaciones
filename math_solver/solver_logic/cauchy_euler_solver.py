from sympy import Eq, dsolve, symbols, latex, solve
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_cauchy_euler(a_str: str, b_str: str, c_str: str, R_str: str) -> dict:
    """
    Resuelve una Ecuación de Cauchy-Euler y proporciona los pasos.
    """
    
    # 1. Parsear y Validar
    a_expr = parse_safe(a_str)
    if a_expr is None: return {'error': f"'a' = '{a_str}' no es válido."}

    b_expr = parse_safe(b_str)
    if b_expr is None: return {'error': f"'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None: return {'error': f"'c' = '{c_str}' no es válido."}
        
    R_expr = parse_safe(R_str)
    if R_expr is None: return {'error': f"R(x) = '{R_str}' no es válida."}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir la Ecuación Original
        ecuacion = Eq((a_expr * (x**2) * y.diff(x, 2)) + (b_expr * x * y.diff(x)) + (c_expr * y), R_expr)
        steps.append(f"1. La ecuación de Cauchy-Euler es: \\( {latex(ecuacion)} \\)")
        
        # 3. Formar la ecuación característica auxiliar
        m = symbols('m')
        ecuacion_aux = Eq(a_expr * m * (m - 1) + b_expr * m + c_expr, 0)
        steps.append(f"2. Se forma la ecuación característica auxiliar suponiendo una solución de la forma \\(y = x^m\\).")
        steps.append(f"   - La ecuación es: \\( {latex(ecuacion_aux)} \\)")

        # 4. Resolver la Ecuación Auxiliar
        raices_aux = solve(ecuacion_aux, m)
        steps.append(f"3. Se resuelven las raíces de la ecuación auxiliar:")
        steps.append(f"   - Las raíces son: \\( m = {latex(raices_aux)} \\)")
        steps.append(f"4. Se construye la solución homogénea (\\(y_h\\)) basada en las raíces.")
        
        # 5. Determinar si es homogénea o no homogénea
        if R_expr == 0:
            steps.append("5. Como la ecuación es homogénea (\\(R(x) = 0\\)), la solución general es igual a la solución homogénea (\\(y = y_h\\)).")
        else:
            steps.append(f"5. Como \\(R(x) \\neq 0\\), se busca una solución particular (\\(y_p\\)) usando métodos como variación de parámetros.")
            steps.append(f"   - La solución general es \\(y = y_h + y_p\\).")

        # 6. Resolver y Formatear
        solucion = dsolve(ecuacion, y)
        solucion_latex = format_latex(solucion)
        steps.append(f"6. La solución final combinada es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}