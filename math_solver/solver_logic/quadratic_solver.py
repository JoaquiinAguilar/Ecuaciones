from sympy import Eq, solve, factor, symbols, discriminant
# Importamos 'x' y nuestras funciones comunes
from .base_solver import x, parse_safe, format_latex

def solve_quadratic(a_str: str, b_str: str, c_str: str) -> dict:
    """
    Resuelve una ecuación cuadrática de la forma:
    ax^2 + bx + c = 0
    
    Devuelve un diccionario con las raíces, la forma factorizada,
    y los pasos para resolverla, formateados en LaTeX, o un mensaje de error.
    """
    
    # 1. Parsear y Validar las Entradas del Usuario
    a_expr = parse_safe(a_str)
    if a_expr is None or a_expr == 0:
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido o es cero."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}

    # 2. Construir la Ecuación y el Polinomio
    try:
        polinomio = (a_expr * x**2) + (b_expr * x) + (c_expr)
        ecuacion = Eq(polinomio, 0)
        
        # --- Generación de Pasos ---
        steps = []
        steps.append(f"1. Se identifica la ecuación cuadrática en la forma \(ax^2 + bx + c = 0\):")
        steps.append(f"   - \(a = {latex(a_expr)}\)")
        steps.append(f"   - \(b = {latex(b_expr)}\)")
        steps.append(f"   - \(c = {latex(c_expr)}\)")
        
        # 3. Calcular el Discriminante
        delta = discriminant(polinomio, x)
        steps.append(f"2. Se calcula el discriminante (\(\Delta = b^2 - 4ac\)):")
        steps.append(f"   - \(\Delta = ({latex(b_expr)})^2 - 4({latex(a_expr)})({latex(c_expr)}) = {latex(delta)}\)")

        # 4. Resolver usando la fórmula cuadrática
        steps.append(f"3. Se aplica la fórmula cuadrática (\(x = \\frac{{-b \\pm \\sqrt{{\Delta}}}}{{2a}}\)):")
        
        # solve() encuentra los valores de 'x' que satisfacen la ecuación
        raices = solve(ecuacion, x)
        
        # factor() intenta factorizar el polinomio
        factorizada = factor(polinomio)
        
        # 5. Formatear la Salida
        raices_latex = format_latex(raices)
        factorizada_latex = format_latex(factorizada)
        
        solucion_html = f"""
            <p class='font-semibold'>Raíces (x):</p>
            {raices_latex}
            <p class='font-semibold mt-4'>Forma Factorizada:</p>
            {factorizada_latex}
        """
        
        # Añadir la solución final a los pasos
        steps.append(f"4. Las raíces de la ecuación son: {raices_latex}")
        
        return {'solucion': solucion_html, 'steps': steps}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}