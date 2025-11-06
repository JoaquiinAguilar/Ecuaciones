from sympy import Eq, dsolve
# Importamos nuestros símbolos y funciones comunes del base_solver
from .base_solver import x, y, parse_safe, format_latex

def solve_bernoulli(P_str: str, Q_str: str, n_str: str) -> dict:
    """
    Resuelve una ecuación de Bernoulli de la forma:
    dy/dx + P(x)*y = Q(x)*y^n
    
    Devuelve un diccionario con la solución formateada en LaTeX
    o un mensaje de error.
    """
    
    # 1. Parsear y Validar las Entradas del Usuario
    # Convertimos los strings "P(x)", "Q(x)" y "n" en expresiones SymPy.
    
    p_expr = parse_safe(P_str)
    if p_expr is None:
        return {'error': f"La expresión P(x) = '{P_str}' no es válida."}

    q_expr = parse_safe(Q_str)
    if q_expr is None:
        return {'error': f"La expresión Q(x) = '{Q_str}' no es válida."}

    n_expr = parse_safe(n_str)
    if n_expr is None:
        return {'error': f"El exponente n = '{n_str}' no es válido."}

    # 2. Construir la Ecuación Diferencial en SymPy
    try:
        # y.diff(x) es la forma en que SymPy representa dy/dx
        # Eq() crea un objeto de Ecuación.
        # Lado izquierdo: dy/dx + P(x)*y
        lado_izquierdo = y.diff(x) + p_expr * y
        
        # Lado derecho: Q(x)*y^n
        lado_derecho = q_expr * (y**n_expr)
        
        # Ecuación completa
        ecuacion = Eq(lado_izquierdo, lado_derecho)

    except Exception as e:
        return {'error': f"Error al construir la ecuación: {e}"}

    # 3. Resolver la Ecuación Simbólicamente
    try:
        # dsolve() es la función mágica de SymPy.
        # Reconoce automáticamente que es una ecuación de Bernoulli
        # y aplica el método de sustitución v = y^(1-n) internamente.
        solucion = dsolve(ecuacion, y)
        
        # 4. Formatear la Salida
        # La solución (ej: Eq(y(x), C1 + ...)) se convierte a LaTeX.
        solucion_latex = format_latex(solucion)
        
        # Devolvemos un diccionario con la clave 'solucion'
        return {'solucion': solucion_latex}

    except Exception as e:
        # Capturamos cualquier error durante la resolución
        # (ej: la ecuación es irresoluble, etc.)
        return {'error': f"Error al resolver la ecuación: {e}"}