from sympy import Eq, dsolve
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_cauchy_euler(a_str: str, b_str: str, c_str: str, R_str: str) -> dict:
    """
    Resuelve una Ecuación de Cauchy-Euler de segundo orden de la forma:
    a*x^2 * y'' + b*x * y' + c*y = R(x)
    
    Donde y'' = y.diff(x, 2) y y' = y.diff(x)
    
    Devuelve un diccionario con la solución formateada en LaTeX
    o un mensaje de error.
    """
    
    # 1. Parsear y Validar las Entradas del Usuario
    # a, b, y c son generalmente constantes numéricas
    a_expr = parse_safe(a_str)
    if a_expr is None:
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}
        
    # R(x) es la función de forzado (puede ser '0')
    R_expr = parse_safe(R_str)
    if R_expr is None:
        return {'error': f"La función R(x) = '{R_str}' no es válida."}

    # 2. Construir la Ecuación Diferencial en SymPy
    try:
        # Definimos las derivadas
        y_pp = y.diff(x, 2)  # Segunda derivada (y'')
        y_p = y.diff(x)     # Primera derivada (y')

        # Lado izquierdo: a*x^2*y'' + b*x*y' + c*y
        lado_izquierdo = (a_expr * (x**2) * y_pp) + (b_expr * x * y_p) + (c_expr * y)
        
        # Lado derecho: R(x)
        lado_derecho = R_expr
        
        # Ecuación completa
        ecuacion = Eq(lado_izquierdo, lado_derecho)

    except Exception as e:
        return {'error': f"Error al construir la ecuación: {e}"}

    # 3. Resolver la Ecuación Simbólicamente
    try:
        # dsolve() de SymPy reconoce esto como una Ecuación de Cauchy-Euler
        # y aplica el método de la ecuación característica (y = x^m)
        # o variación de parámetros si R(x) no es cero.
        solucion = dsolve(ecuacion, y)
        
        # 4. Formatear la Salida
        solucion_latex = format_latex(solucion)
        
        return {'solucion': solucion_latex}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}