from sympy import Eq, solve, factor, symbols
# Importamos 'x' y nuestras funciones comunes
from .base_solver import x, parse_safe, format_latex

def solve_quadratic(a_str: str, b_str: str, c_str: str) -> dict:
    """
    Resuelve una ecuación cuadrática de la forma:
    ax^2 + bx + c = 0
    
    Devuelve un diccionario con las raíces y la forma factorizada,
    formateadas en LaTeX, o un mensaje de error.
    """
    
    # 1. Parsear y Validar las Entradas del Usuario
    # a, b, y c son coeficientes
    a_expr = parse_safe(a_str)
    if a_expr is None:
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}

    # 2. Construir la Ecuación y el Polinomio
    try:
        # El polinomio en sí
        polinomio = (a_expr * x**2) + (b_expr * x) + (c_expr)
        
        # La ecuación (igualada a cero)
        ecuacion = Eq(polinomio, 0)

    except Exception as e:
        return {'error': f"Error al construir la ecuación: {e}"}

    # 3. Resolver y Factorizar
    try:
        # solve() encuentra los valores de 'x' que satisfacen la ecuación
        raices = solve(ecuacion, x)
        
        # factor() intenta factorizar el polinomio
        factorizada = factor(polinomio)
        
        # 4. Formatear la Salida
        raices_latex = format_latex(raices)
        factorizada_latex = format_latex(factorizada)
        
        # Devolvemos un diccionario con ambas soluciones
        # El HTML se encargará de mostrar esto
        solucion_html = f"""
            <p class='font-semibold'>Raíces (x):</p>
            {raices_latex}
            <p class='font-semibold mt-4'>Forma Factorizada:</p>
            {factorizada_latex}
        """
        
        return {'solucion': solucion_html}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}