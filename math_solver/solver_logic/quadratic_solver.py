from sympy import Eq, solve, factor, symbols, discriminant, latex, Float
# Importamos nuestras funciones comunes
from .base_solver import parse_safe, format_latex, create_math_symbols

def solve_quadratic(a_str: str, b_str: str, c_str: str, x0_str: str = "", y0_str: str = "") -> dict:
    """
    Resuelve una ecuación cuadrática de la forma:
    ax^2 + bx + c = 0
    
    Devuelve un diccionario con las raíces, la forma factorizada,
    y los pasos para resolverla, formateados en LaTeX, o un mensaje de error.
    """
    
    # Create fresh symbols for this request
    x, y = create_math_symbols()
    
    # 1. Parsear y Validar las Entradas del Usuario
    a_expr = parse_safe(a_str)
    if a_expr is None or (isinstance(a_expr, (int, float)) and a_expr == 0):
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido o es cero."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}

    # Parsear condiciones iniciales si existen
    x0_expr = None
    y0_expr = None
    has_initial_conditions = False
    
    if x0_str and y0_str:
        x0_expr = parse_safe(x0_str)
        y0_expr = parse_safe(y0_str)
        if x0_expr is not None and y0_expr is not None:
            has_initial_conditions = True

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
        
        # Aplicar condiciones iniciales si existen
        if has_initial_conditions:
            steps.append(f"4. **Aplicando condiciones iniciales:** y({latex(x0_expr)}) = {latex(y0_expr)}")
            # Evaluar cada raíz en la condición inicial
            valid_roots = []
            for root in raices:
                try:
                    # Verificar si la raíz satisface la condición inicial
                    if root.subs(x, x0_expr) == y0_expr:
                        valid_roots.append(root)
                        steps.append(f"   - Raíz {latex(root)} satisface la condición inicial")
                except:
                    pass
            
            if valid_roots:
                solucion_html = f"""
                    <p class='font-semibold'>Raíces que satisfacen y({latex(x0_expr)}) = {latex(y0_expr)}:</p>
                    {format_latex(valid_roots)}
                    <p class='font-semibold mt-4'>Forma Factorizada:</p>
                    {factorizada_latex}
                """
                steps.append(f"5. Raíces válidas: {format_latex(valid_roots)}")
            else:
                solucion_html = f"""
                    <p class='font-semibold'>Raíces (x):</p>
                    {raices_latex}
                    <p class='font-semibold mt-4'>Forma Factorizada:</p>
                    {factorizada_latex}
                    <p class='text-yellow-600 mt-4'>Nota: Ninguna raíz satisface la condición inicial y({latex(x0_expr)}) = {latex(y0_expr)})</p>
                """
                steps.append(f"5. Ninguna raíz satisface la condición inicial")
        else:
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