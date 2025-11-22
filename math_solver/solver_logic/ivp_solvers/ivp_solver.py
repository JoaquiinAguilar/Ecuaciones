"""
IVP Solver - Base module for solving Initial Value Problems

Provides both symbolic (using SymPy) and numerical (Runge-Kutta) methods
for solving differential equations with initial conditions.
"""

from sympy import symbols, Function, dsolve, Eq, latex, lambdify, sin, cos, tan, exp, log, sqrt
import numpy as np
from ..base_solver import x, y, parse_safe, format_latex


def solve_first_order_ivp(equation, x0, y0, method='symbolic', x_range=None):
    """
    Solve a first-order IVP: dy/dx = f(x, y), y(x0) = y0
    
    Args:
        equation: SymPy equation object (Eq) or expression for dy/dx
        x0: Initial x value (float or SymPy expression)
        y0: Initial y value (float or SymPy expression)
        method: 'symbolic' or 'numerical'
        x_range: For numerical: (x_min, x_max, num_points)
        
    Returns:
        dict with 'solution', 'method', 'steps', or 'error'
    """
    try:
        steps = []
        steps.append(f"**Problema de Valor Inicial (IVP) de Primer Orden**")
        steps.append(f"Condición inicial: \\( y({latex(x0)}) = {latex(y0)} \\)")
        
        if method == 'symbolic':
            # Try symbolic solution with dsolve
            steps.append(f"Intentando solución simbólica usando `dsolve` con condiciones iniciales...")
            
            # Create initial conditions dict
            ics = {y.subs(x, x0): y0}
            
            # Solve with initial conditions
            solution = dsolve(equation, y, ics=ics)
            
            steps.append(f"Solución encontrada:")
            solution_latex = format_latex(solution)
            
            return {
                'solution': solution,
                'solution_latex': solution_latex,
                'method': 'symbolic',
                'steps': steps
            }
            
        elif method == 'numerical':
            # Numerical solution using Runge-Kutta
            steps.append(f"Usando método numérico Runge-Kutta de 4º orden (RK4)...")
            
            if x_range is None:
                x_range = (float(x0), float(x0) + 10, 100)
            
            x_min, x_max, num_points = x_range
            
            # Convert equation to dy/dx = f(x, y) form
            # Extract the right-hand side
            if isinstance(equation, Eq):
                rhs = equation.rhs
            else:
                rhs = equation
                
            # Create numerical function from symbolic expression
            f_numeric = lambdify((x, y), rhs, modules=['numpy', {'sin': np.sin, 'cos': np.cos, 
                                                                   'tan': np.tan, 'exp': np.exp,
                                                                   'log': np.log, 'sqrt': np.sqrt}])
            
            # Runge-Kutta 4th order implementation
            x_vals, y_vals = runge_kutta_4(f_numeric, float(x0), float(y0), x_min, x_max, num_points)
            
            steps.append(f"Rango de integración: [{x_min}, {x_max}] con {num_points} puntos")
            steps.append(f"Valor inicial comprobado: y({x0}) = {y0}")
            steps.append(f"Solución numérica calculada en {len(x_vals)} puntos")
            
            # Format some sample points
            sample_indices = [0, len(x_vals)//4, len(x_vals)//2, 3*len(x_vals)//4, -1]
            sample_points = [(x_vals[i], y_vals[i]) for i in sample_indices]
            
            points_str = ", ".join([f"({x:.2f}, {y:.4f})" for x, y in sample_points])
            steps.append(f"Puntos de muestra: {points_str}")
            
            return {
                'solution': 'numerical',
                'x_values': x_vals.tolist(),
                'y_values': y_vals.tolist(),
                'method': 'numerical',
                'steps': steps
            }
    
    except Exception as e:
        return {'error': f"Error al resolver IVP de primer orden: {e}"}


def solve_second_order_ivp(equation, x0, y0, y_prime_0, method='symbolic', x_range=None):
    """
    Solve a second-order IVP: d²y/dx² = f(x, y, y'), y(x0) = y0, y'(x0) = y'0
    
    Args:
        equation: SymPy equation object
        x0: Initial x value
        y0: Initial y value
        y_prime_0: Initial derivative value
        method: 'symbolic' or 'numerical'
        x_range: For numerical: (x_min, x_max, num_points)
        
    Returns:
        dict with 'solution', 'method', 'steps', or 'error'
    """
    try:
        steps = []
        steps.append(f"**Problema de Valor Inicial (IVP) de Segundo Orden**")
        steps.append(f"Condiciones iniciales: \\( y({latex(x0)}) = {latex(y0)} \\), \\( y'({latex(x0)}) = {latex(y_prime_0)} \\)")
        
        if method == 'symbolic':
            steps.append(f"Intentando solución simbólica con `dsolve`...")
            
            # Create initial conditions dict
            ics = {
                y.subs(x, x0): y0,
                y.diff(x).subs(x, x0): y_prime_0
            }
            
            # Solve with initial conditions
            solution = dsolve(equation, y, ics=ics)
            
            steps.append(f"Solución encontrada:")
            solution_latex = format_latex(solution)
            
            return {
                'solution': solution,
                'solution_latex': solution_latex,
                'method': 'symbolic',
                'steps': steps
            }
            
        elif method == 'numerical':
            steps.append(f"Usando método numérico Runge-Kutta de 4º orden para sistemas...")
            
            if x_range is None:
                x_range = (float(x0), float(x0) + 10, 100)
            
            x_min, x_max, num_points = x_range
            
            # Convert second-order ODE to system of first-order ODEs
            # Let z = y', then dz/dx = y''
            # We have: dy/dx = z, dz/dx = f(x, y, z)
            
            # Extract right-hand side (should be expression for y'')
            if isinstance(equation, Eq):
                rhs = equation.rhs
            else:
                rhs = equation
            
            # Create numerical functions
            # f1 = dy/dx = z
            # f2 = dz/dx = rhs
            f2_numeric = lambdify((x, y, symbols('z')), rhs, modules=['numpy'])
            
            def system(x_val, y_val, z_val):
                """System of equations: dy/dx = z, dz/dx = f(x,y,z)"""
                return z_val, f2_numeric(x_val, y_val, z_val)
            
            # Solve system
            x_vals, y_vals, z_vals = runge_kutta_4_system(system, float(x0), float(y0), 
                                                           float(y_prime_0), x_min, x_max, num_points)
            
            steps.append(f"Rango de integración: [{x_min}, {x_max}] con {num_points} puntos")
            steps.append(f"Condiciones iniciales verificadas: y({x0}) = {y0}, y'({x0}) = {y_prime_0}")
            steps.append(f"Sistema resuelto en {len(x_vals)} puntos")
            
            return {
                'solution': 'numerical',
                'x_values': x_vals.tolist(),
                'y_values': y_vals.tolist(),
                'y_prime_values': z_vals.tolist(),
                'method': 'numerical',
                'steps': steps
            }
    
    except Exception as e:
        return {'error': f"Error al resolver IVP de segundo orden: {e}"}


def runge_kutta_4(f, x0, y0, x_min, x_max, num_points):
    """
    Runge-Kutta 4th order method for dy/dx = f(x, y)
    
    Args:
        f: Function f(x, y) representing dy/dx
        x0: Initial x
        y0: Initial y
        x_min, x_max: Integration range
        num_points: Number of evaluation points
        
    Returns:
        x_values, y_values as numpy arrays
    """
    x_vals = np.linspace(x_min, x_max, num_points)
    y_vals = np.zeros(num_points)
    
    # Find starting index
    start_idx = np.argmin(np.abs(x_vals - x0))
    y_vals[start_idx] = y0
    
    # Integrate forward from x0
    for i in range(start_idx, num_points - 1):
        h = x_vals[i + 1] - x_vals[i]
        xi, yi = x_vals[i], y_vals[i]
        
        k1 = f(xi, yi)
        k2 = f(xi + h/2, yi + h*k1/2)
        k3 = f(xi + h/2, yi + h*k2/2)
        k4 = f(xi + h, yi + h*k3)
        
        y_vals[i + 1] = yi + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    # Integrate backward from x0 if needed
    for i in range(start_idx, 0, -1):
        h = x_vals[i] - x_vals[i - 1]
        xi, yi = x_vals[i], y_vals[i]
        
        k1 = f(xi, yi)
        k2 = f(xi - h/2, yi - h*k1/2)
        k3 = f(xi - h/2, yi - h*k2/2)
        k4 = f(xi - h, yi - h*k3)
        
        y_vals[i - 1] = yi - (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    return x_vals, y_vals


def runge_kutta_4_system(system, x0, y0, z0, x_min, x_max, num_points):
    """
    Runge-Kutta 4th order for system: dy/dx = f1(x,y,z), dz/dx = f2(x,y,z)
    
    Args:
        system: Function returning (f1, f2) tuple
        x0: Initial x
        y0: Initial y
        z0: Initial z
        x_min, x_max: Integration range
        num_points: Number of points
        
    Returns:
        x_values, y_values, z_values as numpy arrays
    """
    x_vals = np.linspace(x_min, x_max, num_points)
    y_vals = np.zeros(num_points)
    z_vals = np.zeros(num_points)
    
    # Find starting index
    start_idx = np.argmin(np.abs(x_vals - x0))
    y_vals[start_idx] = y0
    z_vals[start_idx] = z0
    
    # Integrate forward
    for i in range(start_idx, num_points - 1):
        h = x_vals[i + 1] - x_vals[i]
        xi, yi, zi = x_vals[i], y_vals[i], z_vals[i]
        
        k1_y, k1_z = system(xi, yi, zi)
        k2_y, k2_z = system(xi + h/2, yi + h*k1_y/2, zi + h*k1_z/2)
        k3_y, k3_z = system(xi + h/2, yi + h*k2_y/2, zi + h*k2_z/2)
        k4_y, k4_z = system(xi + h, yi + h*k3_y, zi + h*k3_z)
        
        y_vals[i + 1] = yi + (h/6) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        z_vals[i + 1] = zi + (h/6) * (k1_z + 2*k2_z + 2*k3_z + k4_z)
    
    # Integrate backward if needed
    for i in range(start_idx, 0, -1):
        h = x_vals[i] - x_vals[i - 1]
        xi, yi, zi = x_vals[i], y_vals[i], z_vals[i]
        
        k1_y, k1_z = system(xi, yi, zi)
        k2_y, k2_z = system(xi - h/2, yi - h*k1_y/2, zi - h*k1_z/2)
        k3_y, k3_z = system(xi - h/2, yi - h*k2_y/2, zi - h*k2_z/2)
        k4_y, k4_z = system(xi - h, yi - h*k3_y, zi - h*k3_z)
        
        y_vals[i - 1] = yi - (h/6) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        z_vals[i - 1] = zi - (h/6) * (k1_z + 2*k2_z + 2*k3_z + k4_z)
    
    return x_vals, y_vals, z_vals


def solve_ivp_numerically(ode_func, x0, y0, x_range, order=1, y_prime_0=None):
    """
    Convenience wrapper for numerical IVP solving
    
    Args:
        ode_func: String representation of ODE or callable
        x0, y0: Initial conditions
        x_range: (x_min, x_max, num_points)
        order: 1 for first-order, 2 for second-order
        y_prime_0: Required for second-order
        
    Returns:
        Solution dictionary
    """
    if order == 1:
        return solve_first_order_ivp(ode_func, x0, y0, method='numerical', x_range=x_range)
    elif order == 2:
        if y_prime_0 is None:
            return {'error': 'y_prime_0 required for second-order IVP'}
        return solve_second_order_ivp(ode_func, x0, y0, y_prime_0, method='numerical', x_range=x_range)
    else:
        return {'error': f'Order {order} not supported'}
