from sympy import Eq, dsolve, Symbol, Derivative
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_clairaut(f_p_str: str) -> dict:
    """
    Resuelve una Ecuación de Clairaut de la forma:
    y = x*y' + f(y')
    
    El usuario proporciona f(y') como una función de 'p', donde 'p'
    se usa para representar y' (dy/dx).
    
    Devuelve un diccionario con las soluciones (general y singular)
    formateadas en LaTeX o un mensaje de error.
    """
    
    # 1. Definir un símbolo 'p' para representar y'
    # Esto hace que sea más fácil para el usuario escribir f(p)
    p = Symbol('p')
    
    # 2. Parsear y Validar la Entrada del Usuario (f(p))
    try:
        f_p_expr = parse_safe(f_p_str, local_dict={'p': p})
        if f_p_expr is None:
            return {'error': f"La función f(p) = '{f_p_str}' no es válida."}
    except Exception as e:
        return {'error': f"Error al parsear f(p): {e}"}

    # 3. Construir la Ecuación Diferencial en SymPy
    try:
        # Definimos y' (dy/dx)
        y_p = y.diff(x)

        # Sustituimos 'p' en f_p_expr por la derivada real (y_p)
        # Esto nos da f(y')
        f_y_p_expr = f_p_expr.subs(p, y_p)
        
        # Lado izquierdo: y
        lado_izquierdo = y
        
        # Lado derecho: x*y' + f(y')
        lado_derecho = (x * y_p) + f_y_p_expr
        
        # Ecuación completa
        ecuacion = Eq(lado_izquierdo, lado_derecho)

    except Exception as e:
        return {'error': f"Error al construir la ecuación: {e}"}

    # 4. Resolver la Ecuación Simbólicamente
    try:
        # dsolve() de SymPy reconoce esto como una Ecuación de Clairaut.
        # A menudo devuelve una LISTA de soluciones:
        # 1. La solución general (y = C*x + f(C))
        # 2. La(s) solución(es) singular(es) (la envolvente)
        soluciones = dsolve(ecuacion, y)
        
        # 5. Formatear la Salida
        if isinstance(soluciones, list):
            # Múltiples soluciones (general + singular)
            soluciones_latex = []
            for i, sol in enumerate(soluciones):
                tipo = "Solución General" if "C1" in str(sol) else "Solución Singular"
                sol_latex = format_latex(sol)
                soluciones_latex.append(f"<p class='font-semibold mt-2'>{tipo}:</p> {sol_latex}")
            
            # Unir todas las soluciones en un solo bloque HTML
            solucion_final_html = "\n".join(soluciones_latex)
            return {'solucion': solucion_final_html}
            
        elif soluciones:
            # Una sola solución (caso menos común)
            solucion_latex = format_latex(soluciones)
            return {'solucion': solucion_latex}
        else:
            return {'error': "No se pudo encontrar una solución."}

    except Exception as e:
        # Capturar errores si 'p' no se usó correctamente (ej. 'cos(x)' en lugar de 'cos(p)')
        if "free symbol" in str(e):
            return {'error': f"Error al resolver: La función f(p) = '{f_p_str}' no debe contener 'x'. Use 'p' en su lugar."}
        return {'error': f"Error al resolver la ecuación: {e}"}