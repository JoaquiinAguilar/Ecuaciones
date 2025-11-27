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
        ecuacion_latex = latex(ecuacion_original)
        p_latex = latex(p_expr)
        q_latex = latex(q_expr)
        n_latex = latex(n_expr)

        # 1. Mostrar la ecuación original
        steps.append("### 📚 Ecuación de Bernoulli")
        steps.append(f"**Ecuación:** $${ecuacion_latex}$$")
        
        # 2. Identificar P(x), Q(x) y n
        steps.append("**Parámetros Identificados:**")
        steps.append(f"  - $$P(x) = {p_latex}$$")
        steps.append(f"  - $$Q(x) = {q_latex}$$")
        steps.append(f"  - $$n = {n_latex}$$")
        
        if is_ivp:
            steps.append(rf"**Problema de Valor Inicial (IVP)**")
            steps.append(rf"  - Condición inicial: $$y({latex(x0_expr)}) = {latex(y0_expr)}$$")

        # 3. Manejo de Casos Especiales
        if n_expr == 0:
            steps.append("### ⚡ Caso Especial: n = 0")
            steps.append(r"**Teoría:** La ecuación se convierte en lineal:")
            steps.append(r"  - $$y' + P(x)y = Q(x)$$")
            
            # Resolver como ecuación lineal
            ecuacion_lineal = Eq(y.diff(x) + p_expr * y, q_expr)
            steps.append(rf"**Ecuación Lineal:** $${latex(ecuacion_lineal)}$$")
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_lineal, y, ics=ics)
                steps.append("### ✅ Solución Final")
                steps.append(f"  - Solución con IVP: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_lineal, y)
                steps.append("### ✅ Solución Final")
                steps.append(f"  - Solución general: {format_latex(sol_y)}")
            
            solucion_latex = format_latex(sol_y)
            
        elif n_expr == 1:
            steps.append("### ⚡ Caso Especial: n = 1")
            steps.append(r"**Teoría:** La ecuación se convierte en separable:")
            steps.append(r"  - $$y' + P(x)y = Q(x)y \implies y' = (Q(x) - P(x))y$$")
            
            # Resolver como ecuación separable
            q_menos_p = q_expr - p_expr
            steps.append(rf"**Ecuación Separable:** $$\frac{{dy}}{{y}} = ({latex(q_menos_p)})dx$$")
            
            # Integrar ambos lados
            integral_izq = log(y)
            integral_der = integrate(q_menos_p, x)
            sol_separable = Eq(integral_izq, integral_der)
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_original, y, ics=ics)
                steps.append("### ✅ Solución Final")
                steps.append(f"  - Solución con IVP: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_original, y)
                steps.append("### ✅ Solución Final")
                steps.append(f"  - Solución general: {format_latex(sol_y)}")
                
            solucion_latex = format_latex(sol_y)
            
        else:
            # 4. Transformación a Lineal (caso general)
            steps.append("### 🔄 Transformación a Lineal")
            v = Function('v')(x)
            m = 1 - n_expr
            
            steps.append(r"**Teoría:** Para $$n \neq 0, 1$$, usamos la sustitución de Bernoulli.")
            steps.append(r"**Paso 1:** Dividir por $$y^n$$:")
            steps.append(r"  - $$y^{-n}y' + P(x)y^{1-n} = Q(x)$$")
            
            steps.append(rf"**Paso 2:** Sustitución $$v = y^{{1-n}}$$ (donde $$1-n = {latex(m)}$$):")
            steps.append(r"  - $$v' = (1-n)y^{-n}y'$$")
            steps.append(r"  - $$\frac{v'}{1-n} = y^{-n}y'$$")
            
            steps.append(r"**Paso 3:** Ecuación Lineal Resultante:")
            steps.append(r"  - $$\frac{v'}{1-n} + P(x)v = Q(x)$$")
            steps.append(r"  - $$v' + (1-n)P(x)v = (1-n)Q(x)$$")
            
            # Ecuación lineal en v: v' + (1-n)P(x)v = (1-n)Q(x)
            p_lineal = m * p_expr
            q_lineal = m * q_expr
            ecuacion_lineal = Eq(v.diff(x) + p_lineal * v, q_lineal)
            steps.append(rf"**Ecuación Lineal para v(x):** $${latex(ecuacion_lineal)}$$")

            # 5. Resolver la Ecuación Lineal para v(x)
            steps.append(rf"**Paso 4:** Resolver para v(x):")
            sol_v = dsolve(ecuacion_lineal, v)
            steps.append(rf"  - Solución intermedia: $${latex(sol_v)}$$")

            # 6. Sustituir de Vuelta a y(x)
            steps.append("### ✅ Solución Final")
            steps.append(rf"**Paso 5:** Sustituir $$v = y^{{{latex(m)}}}$$:")
            
            # Resolver con o sin IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                sol_y = dsolve(ecuacion_original, y, ics=ics)
                steps.append(f"  - Solución con IVP: {format_latex(sol_y)}")
            else:
                sol_y = dsolve(ecuacion_original, y)
                steps.append(f"  - Solución general: {format_latex(sol_y)}")
                
            solucion_latex = format_latex(sol_y)

        return {'solucion': solucion_latex, 'steps': steps}

    except Exception as e:
        return {'error': f"Error durante la resolución: {e}"}