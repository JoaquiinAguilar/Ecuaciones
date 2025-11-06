from sympy import Eq, dsolve
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_riccati(P_str: str, Q_str: str, R_str: str) -> dict:
    """
    Resuelve una Ecuación de Riccati de la forma:
    y' = P(x)*y^2 + Q(x)*y + R(x)
    
    Devuelve un diccionario con la solución formateada en LaTeX
    o un mensaje de error.
    """
    
    # 1. Parsear y Validar las Entradas del Usuario
    # Convertimos los strings "P(x)", "Q(x)" y "R(x)" en expresiones SymPy.
    
    p_expr = parse_safe(P_str)
    if p_expr is None:
        return {'error': f"La expresión P(x) = '{P_str}' no es válida."}

    q_expr = parse_safe(Q_str)
    if q_expr is None:
        return {'error': f"La expresión Q(x) = '{Q_str}' no es válida."}

    r_expr = parse_safe(R_str)
    if r_expr is None:
        return {'error': f"La expresión R(x) = '{R_str}' no es válida."}

    # 2. Construir la Ecuación Diferencial en SymPy
    try:
        # Lado izquierdo: y' (dy/dx)
        lado_izquierdo = y.diff(x)
        
        # Lado derecho: P(x)*y^2 + Q(x)*y + R(x)
        lado_derecho = (p_expr * y**2) + (q_expr * y) + r_expr
        
        # Ecuación completa
        ecuacion = Eq(lado_izquierdo, lado_derecho)

    except Exception as e:
        return {'error': f"Error al construir la ecuación: {e}"}

    # 3. Resolver la Ecuación Simbólicamente
    try:
        # dsolve() de SymPy intentará resolver la ecuación de Riccati.
        # Estas soluciones pueden ser complejas e involucrar
        # funciones especiales o soluciones implícitas.
        solucion = dsolve(ecuacion, y)
        
        # 4. Formatear la Salida
        solucion_latex = format_latex(solucion)
        
        return {'solucion': solucion_latex}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}