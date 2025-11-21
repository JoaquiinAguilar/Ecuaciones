from sympy import Eq, dsolve, Symbol, Derivative, latex, solve
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_clairaut(f_p_str: str) -> dict:
    """
    Resuelve una Ecuación de Clairaut y proporciona los pasos.
    """
    
    p = Symbol('p')
    C = Symbol('C1') # Usar C1 para consistencia con dsolve

    # 1. Parsear y Validar
    try:
        f_p_expr = parse_safe(f_p_str, local_dict={'p': p})
        if f_p_expr is None:
            return {'error': f"f(p) = '{f_p_str}' no es válida."}
    except Exception as e:
        return {'error': f"Error al parsear f(p): {e}"}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir la Ecuación Original
        y_p = y.diff(x)
        ecuacion = Eq(y, x * y_p + f_p_expr.subs(p, y_p))
        steps.append(r"1. La ecuación de Clairaut es \( y = xy' + f(y') \).")
        steps.append(rf"   - Con \( f(y') \) representada por \( f(p) = {latex(f_p_expr)} \), la ecuación es: \( {latex(ecuacion)} \)")
        # 3. Solución General (manual)
        sol_general = Eq(y, C * x + f_p_expr.subs(p, C))
        steps.append(r"2. La <strong>solución general</strong> se obtiene reemplazando \( y' \) por una constante arbitraria \( C \).")
        steps.append(rf"   - Solución General: \( {latex(sol_general)} \)")
        
        # 4. Solución Singular
        f_p_deriv = f_p_expr.diff(p)
        steps.append(r"3. La <strong>solución singular</strong> (o envolvente) se encuentra derivando con respecto a \( p \) y eliminando el parámetro.")
        steps.append(rf"   - Derivando: \( \frac{{df}}{{dp}} = {latex(f_p_deriv)} \)")
        steps.append(rf"   - La solución singular está dada por: \( x = {latex(-f_p_deriv)} \)")
        steps.append("   - Esta relación junto con la ecuación original define la solución singular.")

        # 5. Resolver y Formatear
        try:
            soluciones = dsolve(ecuacion, y)
            
            if isinstance(soluciones, list):
                soluciones_html = []
                for sol in soluciones:
                    tipo = "Solución General" if "C1" in str(sol) else "Solución Singular"
                    sol_latex = format_latex(sol)
                    soluciones_html.append(f"<p class='font-semibold mt-2'>{tipo}:</p> {sol_latex}")
                solucion_final_html = "\n".join(soluciones_html)
            else:
                solucion_final_html = format_latex(soluciones)

            steps.append(f"4. SymPy resuelve y encuentra: {solucion_final_html}")
            return {'solucion': solucion_final_html, 'steps': steps}
        except Exception as solve_error:
            # Si dsolve falla, mostrar la solución general manualmente
            sol_general_manual = Eq(y, C * x + f_p_expr.subs(p, C))
            sol_latex = format_latex(sol_general_manual)
            steps.append(f"4. Solución general: {sol_latex}")
            steps.append("   Nota: La solución singular requiere eliminación paramétrica manual.")
            return {'solucion': sol_latex, 'steps': steps}

    except Exception as e:
        if "free symbol" in str(e):
            return {'error': f"Error: La función f(p) no debe contener 'x'. Use 'p' en su lugar."}
        return {'error': f"Error durante la resolución: {e}"}