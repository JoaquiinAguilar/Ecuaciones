from sympy import Eq, dsolve, Function, pde_separate_add, latex, simplify, integrate, log
# Importamos nuestros símbolos y funciones comunes del base_solver
from .base_solver import x, y, parse_safe, format_latex

def solve_bernoulli(P_str: str, Q_str: str, n_str: str, x0_str: str = None, y0_str: str = None) -> dict:
    """
    Resuelve una ecuación de Bernoulli y proporciona los pasos.
    
    Args:
        P_str: Función P(x) como string
        Q_str: Función Q(x) como string
        n_str: Exponente n como string
        x0_str: (Opcional) Valor inicial x₀ para IVP
        y0_str: (Opcional) Valor inicial y(x₀) para IVP
    
    Returns:
        dict con 'solucion', 'steps', o 'error'
    """
    
    # 1. Parsear y Validar
    p_expr = parse_safe(P_str)
    if p_expr is None: return {'error': f"P(x) = '{P_str}' no es válido."}

    q_expr = parse_safe(Q_str)
    if q_expr is None: return {'error': f"Q(x) = '{Q_str}' no es válido."}

    n_expr = parse_safe(n_str)
    if n_expr is None: return {'error': f"n = '{n_str}' no es válido."}
    
    # 1b. Validar condiciones iniciales si se proporcionan
    is_ivp = x0_str is not None and y0_str is not None
    if is_ivp:
        x0_expr = parse_safe(x0_str)
        if x0_expr is None: return {'error': f"x₀ = '{x0_str}' no es válido."}
        
        y0_expr = parse_safe(y0_str)
        if y0_expr is None: return {'error': f"y₀ = '{y0_str}' no es válido."}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir Ecuación Original
        ecuacion_original = Eq(y.diff(x) + p_expr * y, q_expr * y**n_expr)
        steps.append(rf"La ecuación de Bernoulli es: \( {latex(ecuacion_original)} \)")
        steps.append(rf"   - Con \( P(x) = {latex(p_expr)} \), \( Q(x) = {latex(q_expr)} \) y \( n = {latex(n_expr)} \).")
        
        # 2b. Mostrar condiciones iniciales si es IVP
        if is_ivp:
            steps.append(rf"**Problema de Valor Inicial (IVP)**:")
            steps.append(rf"   - Condición inicial: \( y({latex(x0_expr)}) = {latex(y0_expr)} \)")

        # 3. Manejo de Casos Especiales
        if n_expr == 0:
            steps.append("3. **Caso Especial: n = 0**")
            steps.append(r"   - La ecuación se convierte en: \( y' + P(x)y = Q(x) \)")
            steps.append("   - Esta es una ecuación diferencial lineal de primer orden.")
            
            # Resolver como ecuación lineal
            ecuacion_lineal = Eq(y.diff(x) + p_expr * y, q_expr)
            steps.append(rf"   - Ecuación lineal: \( {latex(ecuacion_lineal)} \)")
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_lineal, y, ics=ics)
                steps.append(f"   - Solución usando método de ecuación lineal con IVP: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_lineal, y)
                steps.append(f"   - Solución usando método de ecuación lineal: {format_latex(sol_y)}")
            
            solucion_latex = format_latex(sol_y)
            
        elif n_expr == 1:
            steps.append("3. **Caso Especial: n = 1**")
            steps.append(r"   - La ecuación se convierte en: \( y' + P(x)y = Q(x)y \)")
            steps.append(r"   - Reorganizando: \( y' = (Q(x) - P(x))y \)")
            steps.append("   - Esta es una ecuación separable.")
            
            # Resolver como ecuación separable
            q_menos_p = q_expr - p_expr
            steps.append(rf"   - Ecuación separable: \( \frac{{dy}}{{y}} = ({latex(q_menos_p)})dx \)")
            
            # Integrar ambos lados
            integral_izq = log(y)
            integral_der = integrate(q_menos_p, x)
            sol_separable = Eq(integral_izq, integral_der)
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_original, y, ics=ics)
                steps.append(f"   - Solución por separación de variables con IVP: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_original, y)
                steps.append(f"   - Solución por separación de variables: {format_latex(sol_y)}")
                
            solucion_latex = format_latex(sol_y)
            
        else:
            # 4. Transformación a Lineal (caso general)
            steps.append("3. **Caso General: n ≠ 0, 1**")
            v = Function('v')(x)
            m = 1 - n_expr
            steps.append(rf"Se aplica la sustitución \( v = y^{{1-n}} = y^{{{m}}} \). Esto la convierte en una EDO lineal.")
            
            # Ecuación lineal en v: v' + (1-n)P(x)v = (1-n)Q(x)
            p_lineal = m * p_expr
            q_lineal = m * q_expr
            ecuacion_lineal = Eq(v.diff(x) + p_lineal * v, q_lineal)
            steps.append(rf"   - La ecuación lineal transformada para \(v(x)\) es: \( {latex(ecuacion_lineal)} \)")

            # 5. Resolver la Ecuación Lineal para v(x)
            steps.append(rf"Se resuelve la ecuación lineal para \(v(x)\), usualmente con un factor integrante.")
            sol_v = dsolve(ecuacion_lineal, v)
            steps.append(rf"   - La solución para \(v(x)\) es: \( {latex(sol_v)} \)")

            # 6. Sustituir de Vuelta a y(x)
            steps.append(rf"Finalmente, se sustituye \( v = y^{{{m}}} \) para obtener la solución para \(y(x)\).")
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_original, y, ics=ics)
                steps.append(f"   - La solución final con IVP es: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_original, y)
                steps.append(f"   - La solución final es: {format_latex(sol_y)}")
                
            solucion_latex = format_latex(sol_y)

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}