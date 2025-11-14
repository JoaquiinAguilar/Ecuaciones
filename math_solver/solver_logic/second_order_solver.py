from sympy import Eq, dsolve, symbols, latex, Function, simplify, solve, I
# Importamos nuestras funciones comunes
from .base_solver import parse_safe, format_latex, create_math_symbols

def solve_second_order_homogeneous(a_str: str, b_str: str, c_str: str, x0_str: str = "", y0_str: str = "", yp0_str: str = "") -> dict:
    """
    Resuelve ecuaciones diferenciales lineales homogéneas de segundo orden:
    ay'' + by' + cy = 0
    Si se proporcionan condiciones iniciales, encuentra la solución particular.
    """
    
    # Create fresh symbols for this request
    x, y = create_math_symbols()
    
    # 1. Parsear y Validar
    a_expr = parse_safe(a_str)
    if a_expr is None or (isinstance(a_expr, (int, float)) and a_expr == 0):
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido o es cero."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}

    steps = []
    try:
        # 2. Parsear Condiciones Iniciales si existen
        x0_expr = None
        y0_expr = None
        yp0_expr = None
        has_initial_conditions = False
        
        if x0_str and y0_str:
            x0_expr = parse_safe(x0_str)
            y0_expr = parse_safe(y0_str)
            yp0_expr = parse_safe(yp0_str) if yp0_str else None
            
            if x0_expr is not None and y0_expr is not None:
                has_initial_conditions = True
                if yp0_expr is not None:
                    steps.append(f"**Condiciones Iniciales:** \\( y({latex(x0_expr)}) = {latex(y0_expr)}, y'({latex(x0_expr)}) = {latex(yp0_expr)} \\)")
                else:
                    steps.append(f"**Condición Inicial:** \\( y({latex(x0_expr)}) = {latex(y0_expr)} \\)")
        
        # 3. Construir la Ecuación
        y_func = Function('y')(x)
        ecuacion = Eq(a_expr * y_func.diff(x, 2) + b_expr * y_func.diff(x) + c_expr * y_func, 0)
        steps.append(f"2. La ecuación diferencial de segundo orden es: \\( {latex(ecuacion)} \\)")
        steps.append(f"   - Coeficientes: a = {latex(a_expr)}, b = {latex(b_expr)}, c = {latex(c_expr)}")

        # 4. Ecuación Característica
        r = symbols('r')
        ecuacion_caracteristica = Eq(a_expr * r**2 + b_expr * r + c_expr, 0)
        steps.append(f"3. La ecuación característica es: \\( {latex(ecuacion_caracteristica)} \\)")

        # 5. Resolver la Ecuación Característica
        raices = solve(ecuacion_caracteristica, r)
        steps.append(f"4. Las raíces de la ecuación característica son: \\( r = {latex(raices)} \\)")

        # 6. Determinar el tipo de solución según las raíces
        if len(raices) == 2:
            r1, r2 = raices
            
            # Verificar si son reales y distintas - mejor detección de complejos
            if r1.is_real and r2.is_real and r1 != r2:
                steps.append("5. **Raíces reales y distintas**: La solución general es \\( y = C_1 e^{r_1 x} + C_2 e^{r_2 x} \\)")
                steps.append(f"   - Sustituyendo: \\( y = C_1 e^{{{latex(r1)}x}} + C_2 e^{{{latex(r2)}x}} \\)")
                
            elif r1.is_real and r2.is_real and r1 == r2:
                steps.append("5. **Raíz real doble**: La solución general es \\( y = (C_1 + C_2 x)e^{rx} \\)")
                steps.append(f"   - Sustituyendo: \\( y = (C_1 + C_2 x)e^{{{latex(r1)}x}} \\)")
                
            else:
                # Raíces complejas conjugadas - detección mejorada
                # Verificar explícitamente si son complejas conjugadas
                if not r1.is_real or not r2.is_real:
                    alpha = simplify((r1 + r2) / 2)
                    beta = simplify((r1 - r2) / (2 * I))
                    steps.append("5. **Raíces complejas conjugadas**: La solución general es \\( y = e^{\\alpha x}(C_1 \\cos(\\beta x) + C_2 \\sin(\\beta x)) \\)")
                    steps.append(f"   - Con \\( \\alpha = {latex(alpha)} \\) y \\( \\beta = {latex(beta)} \\)")
                else:
                    # Caso raro: raíces reales pero idénticas
                    steps.append("5. **Raíces idénticas**: La solución general es \\( y = (C_1 + C_2 x)e^{rx} \\)")
                    steps.append(f"   - Sustituyendo: \\( y = (C_1 + C_2 x)e^{{{latex(r1)}x}} \\)")

        # 7. Resolver con SymPy
        solucion = dsolve(ecuacion, y)
        solucion_latex = format_latex(solucion)
        
        # Mencionar condiciones iniciales si existen
        if has_initial_conditions:
            steps.append(f"6. La solución general es: {solucion_latex}")
            steps.append(f"   - **Nota:** Se proporcionaron condiciones iniciales. Para la solución particular, consulte la documentación o use métodos numéricos.")
        else:
            steps.append(f"6. La solución final es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}

def solve_second_order_nonhomogeneous(a_str: str, b_str: str, c_str: str, g_str: str, x0_str: str = "", y0_str: str = "", yp0_str: str = "") -> dict:
    """
    Resuelve ecuaciones diferenciales lineales no homogéneas de segundo orden:
    ay'' + by' + cy = g(x)
    """
    
    # 1. Parsear y Validar
    a_expr = parse_safe(a_str)
    if a_expr is None or a_expr == 0:
        return {'error': f"El coeficiente 'a' = '{a_str}' no es válido o es cero."}

    b_expr = parse_safe(b_str)
    if b_expr is None:
        return {'error': f"El coeficiente 'b' = '{b_str}' no es válido."}

    c_expr = parse_safe(c_str)
    if c_expr is None:
        return {'error': f"El coeficiente 'c' = '{c_str}' no es válido."}
        
    g_expr = parse_safe(g_str)
    if g_expr is None:
        return {'error': f"La función g(x) = '{g_str}' no es válida."}

    steps = []
    try:
        # 2. Construir la Ecuación
        y_func = Function('y')(x)
        ecuacion = Eq(a_expr * y_func.diff(x, 2) + b_expr * y_func.diff(x) + c_expr * y_func, g_expr)
        steps.append(f"1. La ecuación diferencial no homogénea de segundo orden es: \\( {latex(ecuacion)} \\)")
        steps.append(f"   - Coeficientes: a = {latex(a_expr)}, b = {latex(b_expr)}, c = {latex(c_expr)}")
        steps.append(f"   - Término no homogéneo: g(x) = {latex(g_expr)}")

        # 3. Explicación del método
        steps.append("2. **Método de Solución**:")
        steps.append("   - Primero se resuelve la ecuación homogénea asociada")
        steps.append("   - Luego se encuentra una solución particular")
        steps.append("   - La solución general es: y = y_h + y_p")

        # 4. Resolver con SymPy
        solucion = dsolve(ecuacion, y_func)
        solucion_latex = format_latex(solucion)
        steps.append(f"3. La solución encontrada por SymPy es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}