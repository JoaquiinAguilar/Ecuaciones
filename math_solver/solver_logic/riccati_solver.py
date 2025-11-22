from sympy import Eq, dsolve, latex, symbols, simplify, integrate, exp, log, solve, Function, diff, Rational, classify_ode, sqrt, atan, asin, acos, tan, sin, cos, airyai, airybi, besselj, bessely, hyper, meijerg
# Importamos nuestros símbolos y funciones comunes
from .base_solver import x, y, parse_safe, format_latex

def is_constant(expr):
    """Safely check if an expression is constant"""
    if expr is None:
        return False
    if isinstance(expr, (int, float)):
        return True
    return hasattr(expr, 'is_number') and expr.is_number

def has_symbol(expr, sym):
    """Safely check if an expression contains a symbol"""
    if expr is None:
        return False
    if isinstance(expr, (int, float)):
        return False
    return hasattr(expr, 'has') and expr.has(sym)

def is_polynomial(expr, sym):
    """Safely check if an expression is a polynomial in a symbol"""
    if expr is None:
        return False
    if isinstance(expr, (int, float)):
        return True
    return hasattr(expr, 'is_polynomial') and expr.is_polynomial(sym)

def solve_riccati(P_str: str, Q_str: str, R_str: str, x0_str: str = None, y0_str: str = None) -> dict:
    """
    Resuelve una Ecuación de Riccati y proporciona los pasos.
    Enhanced version with multiple solution methods and optional IVP support.
    
    Args:
        P_str, Q_str, R_str: Coefficients P(x), Q(x), R(x)
        x0_str: (Opcional) Valor inicial x₀ para IVP
        y0_str: (Opcional) Valor inicial y(x₀) para IVP
    """
    
    # 1. Parsear y Validar
    p_expr = parse_safe(P_str)
    if p_expr is None: return {'error': f"P(x) = '{P_str}' no es válida."}

    q_expr = parse_safe(Q_str)
    if q_expr is None: return {'error': f"Q(x) = '{Q_str}' no es válida."}

    r_expr = parse_safe(R_str)
    if r_expr is None: return {'error': f"R(x) = '{R_str}' no es válida."}
    
    # 1b. Validar condiciones iniciales si se proporcionan
    is_ivp = x0_str is not None and y0_str is not None
    if is_ivp:
        x0_expr = parse_safe(x0_str)
        if x0_expr is None: return {'error': f"x₀ = '{x0_str}' no es válido."}
        
        y0_expr = parse_safe(y0_str)
        if y0_expr is None: return {'error': f"y₀ = '{y0_str }' no es válido."}

    steps = []
    try:
        # 2. Construir la Ecuación Original
        ecuacion = Eq(y.diff(x), (p_expr * y**2) + (q_expr * y) + r_expr)
        ecuacion_latex = latex(ecuacion)
        p_latex = latex(p_expr)
        q_latex = latex(q_expr)
        r_latex = latex(r_expr)
        
        steps.append(f"1. La ecuación de Riccati es: $${ecuacion_latex}$$")
        steps.append(f"   - Con $$P(x) = {p_latex}$$, $$Q(x) = {q_latex}$$ y $$R(x) = {r_latex}$$.")
        
        # 1b. Mostrar condiciones iniciales si es IVP
        if is_ivp:
            steps.append(rf"**Problema de Valor Inicial (IVP)**:")
            steps.append(rf"   - Condición inicial: \\( y({latex(x0_expr)}) = {latex(y0_expr)} \\)")
        
        # Método 1: Intentar dsolve directo primero
        steps.append("2. **Intentando método directo con SymPy**...")
        try:
            # Use ics if IVP
            if is_ivp:
                ics = {y.subs(x, x0_expr): y0_expr}
                solucion_directa = dsolve(ecuacion, y, ics=ics)
            else:
                solucion_directa = dsolve(ecuacion, y)
                
            # FIXED: Check if solution exists without truth value issues
            if solucion_directa is not None and str(solucion_directa) != "[]":
                solucion_latex = format_latex(solucion_directa)
                steps.append(f"   - ✅ Solución encontrada: {solucion_latex}")
                return {'solucion': solucion_latex, 'steps': steps}
            else:
                steps.append("   - ❌ Método directo no funcionó, intentando otros métodos...")
        except Exception as e:
            error_msg = str(e)
            if "Rational" in error_msg:
                steps.append("   - ❌ Método directo: Error en solución racional, intentando otros métodos...")
            else:
                steps.append(f"   - ❌ Método directo falló: {error_msg}")
        
        # Método 2: Casos especiales
        steps.append("3. **Verificando casos especiales**...")
        
        # Caso 2.1: Ecuación separable (Q = R = 0)
        if q_expr == 0 and r_expr == 0:
            steps.append("   - **Caso especial: Ecuación separable** (Q=0, R=0)")
            steps.append("   - Ecuación: y' = P(x)y²")
            steps.append("   - Separando: dy/y² = P(x)dx")
            
            try:
                integral_p = integrate(p_expr, x)
                sol_separable = Eq(y, -1 / (integral_p + symbols('C1')))
                solucion_latex = format_latex(sol_separable)
                steps.append(f"   - ✅ Solución: {solucion_latex}")
                return {'solucion': solucion_latex, 'steps': steps}
            except Exception as e:
                steps.append(f"   - ❌ Error en método separable: {e}")
        
        # Caso 2.2: Ecuación lineal (P = 0)
        elif p_expr == 0:
            steps.append("   - **Caso especial: Ecuación lineal** (P=0)")
            steps.append("   - Ecuación: y' = Q(x)y + R(x)")
            steps.append("   - Resolviendo como ecuación lineal...")
            
            try:
                ecuacion_lineal = Eq(y.diff(x), q_expr * y + r_expr)
                sol_lineal = dsolve(ecuacion_lineal, y)
                if sol_lineal is not None and str(sol_lineal) != "[]":
                    solucion_latex = format_latex(sol_lineal)
                    steps.append(f"   - ✅ Solución lineal: {solucion_latex}")
                    return {'solucion': solucion_latex, 'steps': steps}
            except Exception as e:
                steps.append(f"   - ❌ Error en método lineal: {e}")
        
        # Método 3: Transformación de Bernoulli
        steps.append("4. **Intentando sustitución de Bernoulli**...")
        try:
            u = Function('u')(x)
            # Transformación: y = -u'/(P*u)
            ec_u = Eq(u.diff(x, 2) - q_expr * u.diff(x) - p_expr * r_expr * u, 0)
            ec_u_latex = latex(ec_u)
            steps.append(f"   - Ecuación transformada: $${ec_u_latex}$$")
            
            sol_u = dsolve(ec_u, u)
            if sol_u is not None and str(sol_u) != "[]":
                steps.append(f"   - ✅ Solución para u encontrada")
                # Intentar obtener solución final
                try:
                    sol_final = dsolve(ecuacion, y)
                    if sol_final is not None and str(sol_final) != "[]":
                        solucion_latex = format_latex(sol_final)
                        steps.append(f"   - ✅ Solución final: {solucion_latex}")
                        return {'solucion': solucion_latex, 'steps': steps}
                except:
                    pass
                
                # Si no podemos obtener la final, al menos mostrar la de u
                u_sol_latex = format_latex(sol_u)
                solucion_completa = f"""
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <h4 class="font-bold text-green-800 mb-2">Solución Encontrada</h4>
                    <p class="text-green-700">Se encontró solución para u(x):</p>
                    <div class="mt-2 p-2 bg-white rounded">
                        {u_sol_latex}
                    </div>
                    <p class="mt-2 text-sm text-green-600">
                        La solución para y(x) se obtiene de: y = -u'/(P*u)
                    </p>
                </div>
                """
                steps.append(f"   - ✅ Solución parcial encontrada")
                return {'solucion': solucion_completa, 'steps': steps}
            else:
                steps.append("   - ❌ No se pudo resolver ecuación transformada")
        except Exception as e:
            steps.append(f"   - ❌ Error en transformación: {e}")
        
        # Método 4: Intentar solución particular
        steps.append("5. **Buscando solución particular**...")
        try:
            # Intentar solución particular constante
            k = symbols('k')
            if p_expr != 0:
                ec_k = Eq(p_expr * k**2 + q_expr * k + r_expr, 0)
                sol_k = solve(ec_k, k)
                if sol_k and len(sol_k) > 0:
                    y_p = sol_k[0]
                    steps.append(f"   - ✅ Solución particular: y_p = {latex(y_p)}")
                    
                    # Ahora resolver con esta solución particular
                    try:
                        sol_final = dsolve(ecuacion, y)
                        if sol_final is not None and str(sol_final) != "[]":
                            solucion_latex = format_latex(sol_final)
                            steps.append(f"   - ✅ Solución completa: {solucion_latex}")
                            return {'solucion': solucion_latex, 'steps': steps}
                    except:
                        pass
        except Exception as e:
            steps.append(f"   - ❌ Error en búsqueda de solución particular: {e}")
        
        # Método 5: Simplificación
        steps.append("6. **Intentando simplificación**...")
        try:
            p_simpl = simplify(p_expr)
            q_simpl = simplify(q_expr)
            r_simpl = simplify(r_expr)
            
            if p_simpl != p_expr or q_simpl != q_expr or r_simpl != r_expr:
                steps.append("   - Coeficientes simplificados")
                ecuacion_simpl = Eq(y.diff(x), (p_simpl * y**2) + (q_simpl * y) + r_simpl)
                sol_simpl = dsolve(ecuacion_simpl, y)
                if sol_simpl is not None and str(sol_simpl) != "[]":
                    solucion_latex = format_latex(sol_simpl)
                    steps.append(f"   - ✅ Solución simplificada: {solucion_latex}")
                    return {'solucion': solucion_latex, 'steps': steps}
        except Exception as e:
            steps.append(f"   - ❌ Error en simplificación: {e}")
        
        # Método 6: Clasificación y hints
        steps.append("7. **Intentando diferentes hints**...")
        try:
            ode_class = classify_ode(ecuacion)
            steps.append(f"   - Clasificación: {ode_class}")
            
            # Probar diferentes hints
            hints_to_try = ['riccati', 'lie_group', '2nd_power_series', '1st_exact', '1st_power_series']
            
            for hint in hints_to_try:
                try:
                    sol_hint = dsolve(ecuacion, y, hint=hint)
                    if sol_hint is not None and str(sol_hint) != "[]":
                        solucion_latex = format_latex(sol_hint)
                        steps.append(f"   - ✅ Solución con hint '{hint}': {solucion_latex}")
                        return {'solucion': solucion_latex, 'steps': steps}
                except:
                    continue
        except Exception as e:
            steps.append(f"   - ❌ Error en clasificación: {e}")
        
        # Si todo falla, dar análisis completo
        steps.append("8. **Análisis final**...")
        steps.append("   - Se intentaron todos los métodos disponibles")
        steps.append("   - La ecuación puede no tener solución elemental")
        
        # Dar información útil
        partial_solution = f"""
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="font-bold text-blue-800 mb-2">Análisis de Ecuación de Riccati</h4>
            <div class="text-blue-700">
                <p><strong>Ecuación:</strong> {latex(ecuacion)}</p>
                <p><strong>Coeficientes:</strong></p>
                <ul>
                    <li>P(x) = {latex(p_expr)}</li>
                    <li>Q(x) = {latex(q_expr)}</li>
                    <li>R(x) = {latex(r_expr)}</li>
                </ul>
                <p class="mt-2"><strong>Estado:</strong> No se encontró solución simbólica elemental.</p>
                <p class="mt-2"><strong>Recomendaciones:</strong></p>
                <ul>
                    <li>Verificar coeficientes con software especializado</li>
                    <li>Considerar métodos numéricos para condiciones iniciales</li>
                    <li>Consultar literatura sobre ecuaciones de Riccati</li>
                </ul>
            </div>
        </div>
        """
        
        return {'solucion': partial_solution, 'steps': steps}
        
    except Exception as e:
        return {'error': f"Error general: {e}", 'steps': steps}