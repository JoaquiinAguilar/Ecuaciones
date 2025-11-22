from sympy import Eq, dsolve, symbols, latex, Function, simplify, solve
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, parse_safe, format_latex

def solve_second_order_homogeneous(a_str: str, b_str: str, c_str: str, 
                                    x0_str: str = None, y0_str: str = None, y_prime_0_str: str = None) -> dict:
    """
    Resuelve ecuaciones diferenciales lineales homogéneas de segundo orden:
    ay'' + by' + cy = 0
    
    Args:
        a_str, b_str, c_str: Coeficientes de la ecuación
        x0_str: (Opcional) Valor inicial x₀ para IVP
        y0_str: (Opcional) Valor inicial y(x₀) para IVP 
        y_prime_0_str: (Opcional) Valor inicial y'(x₀) para IVP
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
    
    # 1b. Validar condiciones iniciales si se proporcionan
    is_ivp = x0_str is not None and y0_str is not None and y_prime_0_str is not None
    if is_ivp:
        x0_expr = parse_safe(x0_str)
        if x0_expr is None: return {'error': f"x₀ = '{x0_str}' no es válido."}
        
        y0_expr = parse_safe(y0_str)
        if y0_expr is None: return {'error': f"y₀ = '{y0_str}' no es válido."}
        
        y_prime_0_expr = parse_safe(y_prime_0_str)
        if y_prime_0_expr is None: return {'error': f"y'₀ = '{y_prime_0_str}' no es válido."}

    steps = []
    try:
        # 2. Construir la Ecuación
        y_func = Function('y')(x)
        ecuacion = Eq(a_expr * y_func.diff(x, 2) + b_expr * y_func.diff(x) + c_expr * y_func, 0)
        steps.append(rf"1. La ecuación diferencial de segundo orden es: \( {latex(ecuacion)} \)")
        steps.append(f"   - Coeficientes: a = {latex(a_expr)}, b = {latex(b_expr)}, c = {latex(c_expr)}")
        
        # 2b. Mostrar condiciones iniciales si es IVP
        if is_ivp:
            steps.append(rf"**Problema de Valor Inicial (IVP)**:")
            steps.append(rf"   - Condición inicial: \( y({latex(x0_expr)}) = {latex(y0_expr)} \)")
            steps.append(rf"   - Condición inicial (derivada): \( y'({latex(x0_expr)}) = {latex(y_prime_0_expr)} \)")

        # 3. Ecuación Característica
        r = symbols('r')
        ecuacion_caracteristica = Eq(a_expr * r**2 + b_expr * r + c_expr, 0)
        steps.append(rf"2. La ecuación característica es: \( {latex(ecuacion_caracteristica)} \)")

        # 4. Resolver la Ecuación Característica
        raices = solve(ecuacion_caracteristica, r)
        steps.append(rf"3. Las raíces de la ecuación característica son: \( r = {latex(raices)} \)")

        # 5. Determinar el tipo de solución según las raíces
        if len(raices) == 2:
            r1, r2 = raices
            
            # Verificar si son reales y distintas
            if r1.is_real and r2.is_real and r1 != r2:
                steps.append(r"4. **Raíces reales y distintas**: La solución general es \( y = C_1 e^{r_1 x} + C_2 e^{r_2 x} \)")
                steps.append(rf"   - Sustituyendo: \( y = C_1 e^{{{latex(r1)}x}} + C_2 e^{{{latex(r2)}x}} \)")
                
            elif r1.is_real and r2.is_real and r1 == r2:
                steps.append(r"4. **Raíz real doble**: La solución general es \( y = (C_1 + C_2 x)e^{rx} \)")
                steps.append(rf"   - Sustituyendo: \( y = (C_1 + C_2 x)e^{{{latex(r1)}x}} \)")
                
            else:
                # Raíces complejas conjugadas
                alpha = simplify((r1 + r2) / 2)
                beta = simplify((r1 - r2) / (2 * symbols('I')))
                steps.append(r"4. **Raíces complejas conjugadas**: La solución general es \( y = e^{\alpha x}(C_1 \cos(\beta x) + C_2 \sin(\beta x)) \)")
                steps.append(rf"   - Con \( \alpha = {latex(alpha)} \) y \( \beta = {latex(beta)} \)")

        # 6. Resolver con SymPy
        if is_ivp:
            ics = {
                y_func.subs(x, x0_expr): y0_expr,
                y_func.diff(x).subs(x, x0_expr): y_prime_0_expr
            }
            solucion = dsolve(ecuacion, y_func, ics=ics)
            steps.append(f"5. La solución con IVP es: {format_latex(solucion)}")
        else:
            solucion = dsolve(ecuacion, y_func)
            steps.append(f"5. La solución general es: {format_latex(solucion)}")
            
        solucion_latex = format_latex(solucion)

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}

def solve_second_order_nonhomogeneous(a_str: str, b_str: str, c_str: str, g_str: str,
                                       x0_str: str = None, y0_str: str = None, y_prime_0_str: str = None) -> dict:
    """
    Resuelve ecuaciones diferenciales lineales no homogéneas de segundo orden:
    ay'' + by' + cy = g(x)
    
    Args:
        a_str, b_str, c_str: Coeficientes de la ecuación
        g_str: Función g(x) lado derecho
        x0_str: (Opcional) Valor inicial x₀ para IVP
        y0_str: (Opcional) Valor inicial y(x₀) para IVP
        y_prime_0_str: (Opcional) Valor inicial y'(x₀) para IVP
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
    
    # 1b. Validar condiciones iniciales
    is_ivp = x0_str is not None and y0_str is not None and y_prime_0_str is not None
    if is_ivp:
        x0_expr = parse_safe(x0_str)
        if x0_expr is None: return {'error': f"x₀ = '{x0_str}' no es válido."}
        
        y0_expr = parse_safe(y0_str)
        if y0_expr is None: return {'error': f"y₀ = '{y0_str}' no es válido."}
        
        y_prime_0_expr = parse_safe(y_prime_0_str)
        if y_prime_0_expr is None: return {'error': f"y'₀ = '{y_prime_0_str}' no es válido."}

    steps = []
    try:
        # 2. Construir la Ecuación
        y_func = Function('y')(x)
        ecuacion = Eq(a_expr * y_func.diff(x, 2) + b_expr * y_func.diff(x) + c_expr * y_func, g_expr)
        steps.append(rf"1. La ecuación diferencial no homogénea de segundo orden es: \( {latex(ecuacion)} \)")
        steps.append(f"   - Coeficientes: a = {latex(a_expr)}, b = {latex(b_expr)}, c = {latex(c_expr)}")
        steps.append(f"   - Término no homogéneo: g(x) = {latex(g_expr)}")
        
        # 2b. Mostrar condiciones iniciales si es IVP
        if is_ivp:
            steps.append(rf"**Problema de Valor Inicial (IVP)**:")
            steps.append(rf"   - \( y({latex(x0_expr)}) = {latex(y0_expr)} \)")
            steps.append(rf"   - \( y'({latex(x0_expr)}) = {latex(y_prime_0_expr)} \)")

        # 3. Explicación del método
        steps.append("2. **Método de Solución**:")
        steps.append("   - Primero se resuelve la ecuación homogénea asociada")
        steps.append("   - Luego se encuentra una solución particular")
        steps.append("   - La solución general es: y = y_h + y_p")

        # 4. Resolver con SymPy
        if is_ivp:
            ics = {
                y_func.subs(x, x0_expr): y0_expr,
                y_func.diff(x).subs(x, x0_expr): y_prime_0_expr
            }
            solucion = dsolve(ecuacion, y_func, ics=ics)
            steps.append(f"3. La solución con IVP encontrada por SymPy es: {format_latex(solucion)}")
        else:
            solucion = dsolve(ecuacion, y_func)
            steps.append(f"3. La solución general encontrada por SymPy es: {format_latex(solucion)}")
            
        solucion_latex = format_latex(solucion)

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error al resolver la ecuación: {e}"}