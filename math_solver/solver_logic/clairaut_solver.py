from sympy import Eq, dsolve, Symbol, Derivative, latex, solve, simplify
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def solve_clairaut(f_p_str: str) -> dict:
    """
    Resuelve una Ecuación de Clairaut y proporciona los pasos.
    """
    
    p = Symbol('p')
    C = Symbol('C1') # Usar C1 para consistencia con dsolve

    # 1. Parsear y Validar
    try:
        f_p_expr = parse_safe(f_p_str, local_dict={'p': p})
        if f_p_expr is None:
            return {'error': f"f(p) = '{f_p_str}' no es válida."}
    except Exception as e:
        return {'error': f"Error al parsear f(p): {e}"}

    # --- Inicio de la Generación de Pasos ---
    steps = []
    try:
        # 2. Construir la Ecuación Original
        y_p = y.diff(x)
        ecuacion = Eq(y, x * y_p + f_p_expr.subs(p, y_p))
        
        # Header
        steps.append("### 📚 Ecuación de Clairaut")
        steps.append(rf"**Ecuación:** $$y = xy' + f(y')$$")
        steps.append(rf"  - Con $$f(p) = {latex(f_p_expr)}$$")
        steps.append(rf"  - Ecuación completa: $${latex(ecuacion)}$$")

        # 3. Solución General (manual)
        steps.append("### ⚡ Solución General")
        sol_general = Eq(y, C * x + f_p_expr.subs(p, C))
        steps.append(r"**Teoría:** La solución general es una familia de rectas dada por $$y = Cx + f(C)$$.")
        steps.append(rf"**Solución General:** $${latex(sol_general)}$$")
        
        # 4. Solución Singular (Método de Lagrange)
        steps.append("### 🌟 Solución Singular (Método de Lagrange)")
        steps.append(r"**Teoría:** La solución singular es la envolvente de la familia de rectas. Se obtiene usando ecuaciones paramétricas:")
        steps.append(r"  - $$x = -f'(p)$$")
        steps.append(r"  - $$y = f(p) - p \cdot f'(p)$$")
        
        # Paso 1: Derivar f(p)
        f_p_deriv = f_p_expr.diff(p)
        steps.append(rf"**Paso 1:** Calcular $$f'(p)$$:")
        steps.append(rf"  - $$f'(p) = {latex(f_p_deriv)}$$")
        
        # Paso 2: Obtener x(p)
        x_param = -f_p_deriv
        steps.append(rf"**Paso 2:** Obtener $$x(p)$$:")
        steps.append(rf"  - $$x = -({latex(f_p_deriv)}) = {latex(x_param)}$$")
        
        # Paso 3: Obtener y(p)
        y_param = f_p_expr - p * f_p_deriv
        steps.append(rf"**Paso 3:** Obtener $$y(p)$$:")
        steps.append(rf"  - $$y = {latex(f_p_expr)} - p({latex(f_p_deriv)})$$")
        steps.append(rf"  - $$y = {latex(simplify(y_param))}$$")
        
        # Paso 4: Eliminar parámetro (si es posible)
        steps.append(rf"**Paso 4:** Eliminar el parámetro $$p$$ (si es posible) para obtener $$y(x)$$.")
        
        solucion_singular_latex = ""
        try:
            # Intentar despejar p de x = -f'(p)
            p_solutions = solve(Eq(x, x_param), p)
            if p_solutions:
                steps.append(rf"  - Despejando $$p$$ de la ecuación de $$x$$: $$p = {latex(p_solutions[0])}$$ (una de las soluciones)")
                y_final = y_param.subs(p, p_solutions[0])
                solucion_singular_latex = latex(Eq(y, simplify(y_final)))
                steps.append(rf"  - Sustituyendo en $$y(p)$$: $$y = {solucion_singular_latex}$$")
            else:
                steps.append(r"  - No se pudo despejar $$p$$ explícitamente. La solución queda en forma paramétrica.")
                solucion_singular_latex = rf"\begin{{cases}} x = {latex(x_param)} \\ y = {latex(simplify(y_param))} \end{{cases}}"
        except:
            steps.append(r"  - Cálculo complejo, manteniendo forma paramétrica.")
            solucion_singular_latex = rf"\begin{{cases}} x = {latex(x_param)} \\ y = {latex(simplify(y_param))} \end{{cases}}"

        # 5. Resolver y Formatear Final
        steps.append("### ✅ Solución Final")
        
        solucion_final_html = f"<p class='font-semibold mt-2'>Solución General:</p> $${latex(sol_general)}$$"
        if solucion_singular_latex:
             solucion_final_html += f"<br><p class='font-semibold mt-2'>Solución Singular:</p> $${solucion_singular_latex}$$"
        
        return {'solucion': solucion_final_html, 'steps': steps}

    except Exception as e:
        if "free symbol" in str(e):
            return {'error': f"Error: La función f(p) no debe contener 'x'. Use 'p' en su lugar."}
        return {'error': f"Error durante la resolución: {e}"}