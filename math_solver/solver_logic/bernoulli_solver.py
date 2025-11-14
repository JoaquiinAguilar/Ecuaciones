from sympy import Eq, dsolve, Function, latex, simplify, integrate, log, solve, symbols, Equality
# Importamos nuestras funciones comunes del base_solver
from .base_solver import parse_safe, format_latex, create_math_symbols

def solve_bernoulli(P_str: str, Q_str: str, n_str: str, x0_str: str = "", y0_str: str = "") -> dict:
    """
    Resuelve una Ecuación de Bernoulli y proporciona los pasos.
    Si se proporcionan condiciones iniciales, encuentra la solución particular.
    """
    
    # Create fresh symbols for this request
    x, y = create_math_symbols()
    
    # 1. Parsear y Validar
    p_expr = parse_safe(P_str)
    if p_expr is None: 
        return {'error': f"P(x) = '{P_str}' no es válido."}

    q_expr = parse_safe(Q_str)
    if q_expr is None: 
        return {'error': f"Q(x) = '{Q_str}' no es válido."}

    n_expr = parse_safe(n_str)
    if n_expr is None: 
        return {'error': f"n = '{n_str}' no es válido."}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Parsear Condiciones Iniciales si existen
        x0_expr = None
        y0_expr = None
        has_initial_conditions = False
        
        if x0_str and y0_str:
            x0_expr = parse_safe(x0_str)
            y0_expr = parse_safe(y0_str)
            if x0_expr is not None and y0_expr is not None:
                has_initial_conditions = True
                steps.append(f"**Condiciones Iniciales:** \\( y({latex(x0_expr)}) = {latex(y0_expr)} \\)")
        
        # 3. Construir Ecuación Original
        ecuacion_original = Eq(y.diff(x) + p_expr * y, q_expr * y**n_expr)
        steps.append(f"La ecuación de Bernoulli es: \\( {latex(ecuacion_original)} \\)")
        steps.append(f"   - Con \\( P(x) = {latex(p_expr)} \\), \\( Q(x) = {latex(q_expr)} \\) y \\( n = {latex(n_expr)} \\).")

        # 4. Manejo de Casos Especiales
        if n_expr == 0:
            steps.append("3. **Caso Especial: n = 0**")
            steps.append("   - La ecuación se convierte en: \\( y' + P(x)y = Q(x) \\)")
            steps.append("   - Esta es una ecuación diferencial lineal de primer orden.")
            
            # Resolver como ecuación lineal
            ecuacion_lineal = Eq(y.diff(x) + p_expr * y, q_expr)
            steps.append(f"   - Ecuación lineal: \\( {latex(ecuacion_lineal)} \\)")
            
            sol_y = dsolve(ecuacion_lineal, y)
            solucion_latex = format_latex(sol_y)
            steps.append(f"   - Solución usando método de ecuación lineal: {solucion_latex}")
            
        elif n_expr == 1:
            steps.append("3. **Caso Especial: n = 1**")
            steps.append("   - La ecuación se convierte en: \\( y' + P(x)y = Q(x)y \\)")
            steps.append("   - Reorganizando: \\( y' = (Q(x) - P(x))y \\)")
            steps.append("   - Esta es una ecuación separable.")
            
            # Resolver como ecuación separable
            q_menos_p = q_expr - p_expr
            steps.append(f"   - Ecuación separable: \\( \\frac{{dy}}{{y}} = ({latex(q_menos_p)})dx \\)")
            
            # Integrar ambos lados
            integral_izq = log(y)
            integral_der = integrate(q_menos_p, x)
            sol_separable = Eq(integral_izq, integral_der)
            
            sol_y = dsolve(ecuacion_original, y)
            solucion_latex = format_latex(sol_y)
            steps.append(f"   - Solución por separación de variables: {solucion_latex}")
            
        else:
            # 4. Transformación a Lineal (caso general)
            steps.append("3. **Caso General: n ≠ 0, 1**")
            v = Function('v')(x)
            m = 1 - n_expr
            steps.append(f"Se aplica la sustitución \\( v = y^{{1-n}} = y^{{{m}}} \\). Esto la convierte en una EDO lineal.")
            
            # Ecuación lineal en v: v' + (1-n)P(x)v = (1-n)Q(x)
            p_lineal = m * p_expr
            q_lineal = m * q_expr
            ecuacion_lineal = Eq(v.diff(x) + p_lineal * v, q_lineal)
            steps.append(f"   - La ecuación lineal transformada para \\(v(x)\\) es: \\( {latex(ecuacion_lineal)} \\)")

            # 5. Resolver la Ecuación Lineal para v(x)
            steps.append(f"Se resuelve la ecuación lineal para \\(v(x)\\), usualmente con un factor integrante.")
            sol_v = dsolve(ecuacion_lineal, v)
            steps.append(f"   - La solución para \\(v(x)\\) es: \\( {latex(sol_v)} \\)")

            # 6. Sustituir de Vuelta a y(x)
            steps.append(f"Finalmente, se sustituye \\( v = y^{{{m}}} \\) para obtener la solución para \\(y(x)\\).")
            sol_y = dsolve(ecuacion_original, y)
            
            # Aplicar condiciones iniciales si existen
            if has_initial_conditions:
                try:
                    C1 = symbols('C1')
                    # Extraer la solución del objeto Equality si es necesario
                    if hasattr(sol_y, 'rhs'):
                        sol_expr = getattr(sol_y, 'rhs')
                    else:
                        sol_expr = sol_y
                    
                    # Resolver para C1 usando condiciones iniciales - manejar caso donde y0_expr podría ser None
                    if x0_expr is not None and y0_expr is not None:
                        equation_for_C1 = sol_expr.subs(x, x0_expr) - y0_expr
                        sol_for_C1 = solve(equation_for_C1, C1)
                        if sol_for_C1 and len(sol_for_C1) > 0:
                            sol_y_with_ic = sol_expr.subs(C1, sol_for_C1[0])
                            sol_y_with_ic_eq = Eq(y, sol_y_with_ic)
                            solucion_latex = format_latex(sol_y_with_ic_eq)
                            steps.append(f"   - **Aplicando condiciones iniciales:**")
                            steps.append(f"   - Solución particular: {solucion_latex}")
                        else:
                            solucion_latex = format_latex(sol_y)
                            steps.append(f"   - Solución general: {solucion_latex}")
                            steps.append(f"   - **Nota:** No se pudieron resolver las condiciones iniciales")
                    else:
                        solucion_latex = format_latex(sol_y)
                        steps.append(f"   - Solución general: {solucion_latex}")
                        steps.append(f"   - **Nota:** Condiciones iniciales incompletas")
                except Exception as ic_error:
                    solucion_latex = format_latex(sol_y)
                    steps.append(f"   - Solución general: {solucion_latex}")
                    steps.append(f"   - **Nota:** No se pudieron aplicar las condiciones iniciales: {ic_error}")
            else:
                solucion_latex = format_latex(sol_y)
                steps.append(f"   - La solución final es: {solucion_latex}")

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}