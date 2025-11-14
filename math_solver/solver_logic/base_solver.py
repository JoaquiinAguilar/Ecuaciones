from sympy import sympify, latex, symbols, Function, SympifyError, sin, cos, tan, exp, log, asin, acos, atan, sqrt, Float

# --- Diccionario de Funciones Permitidas para parse_safe ---
# Permite que los usuarios usen funciones matemáticas comunes
ALLOWED_FUNCTIONS = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'exp': exp, 'log': log, 'ln': log,
    'sqrt': sqrt
}

def create_math_symbols():
    """
    Create fresh mathematical symbols for each request to avoid race conditions.
    Returns a tuple of (x, y) symbols.
    """
    x = symbols('x')
    y = Function('y')(x)
    return x, y

def parse_safe(expr_str: str, local_dict=None, max_length=1000):
    """
    Convierte de forma segura un string de usuario en una expresión SymPy.
    
    Usa sympify con un manejo de errores estricto y funciones permitidas.
    Devuelve la expresión SymPy si es válida, o None si falla.
    """
    if not expr_str:
        return None
    
    # Input validation to prevent memory bombs
    if len(expr_str) > max_length:
        return None
    
    # Basic security check - prevent dangerous imports
    dangerous_patterns = ['__import__', 'eval', 'exec', 'open', 'file', 'system', 'subprocess']
    for pattern in dangerous_patterns:
        if pattern in expr_str.lower():
            return None
    
    try:
        # Combinar el diccionario local con las funciones permitidas
        if local_dict is None:
            local_dict = {}
        combined_dict = {**ALLOWED_FUNCTIONS, **local_dict}
        
        # Usamos sympify para convertir el string en una expresión matemática.
        # Ej: "x**2 + 1" -> x**2 + 1 (objeto SymPy)
        expr = sympify(expr_str, locals=combined_dict)
        return expr
    except (SympifyError, TypeError, AttributeError, ValueError):
        # Si el usuario escribe algo inválido como "x + / * y",
        # sympify lanzará un error. Lo capturamos y devolvemos None.
        return None
    
    # Input validation to prevent memory bombs
    if len(expr_str) > max_length:
        return None
    
    # Basic security check - prevent dangerous imports
    dangerous_patterns = ['__import__', 'eval', 'exec', 'open', 'file', 'system', 'subprocess']
    for pattern in dangerous_patterns:
        if pattern in expr_str.lower():
            return None
    
    try:
        # Combinar el diccionario local con las funciones permitidas
        if local_dict is None:
            local_dict = {}
        combined_dict = {**ALLOWED_FUNCTIONS, **local_dict}
        
        # Usamos sympify para convertir el string en una expresión matemática.
        # Ej: "x**2 + 1" -> x**2 + 1 (objeto SymPy)
        expr = sympify(expr_str, locals=combined_dict)
        return expr
    except (SympifyError, TypeError, AttributeError, ValueError):
        # Si el usuario escribe algo inválido como "x + / * y",
        # sympify lanzará un error. Lo capturamos y devolvemos None.
        return None

def format_latex(expr) -> str:
    """
    Convierte una expresión SymPy (como una solución) en un string de LaTeX.
    
    Esto permite que MathJax lo renderice bellamente en el frontend.
    """
    try:
        # latex() es la función de SymPy que genera el código LaTeX.
        return f"$${latex(expr)}$$"
    except Exception:
        # Si hay algún problema, devolvemos un string de error.
        return "Error al formatear LaTeX."