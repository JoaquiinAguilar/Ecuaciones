from django.test import TestCase, Client
from django.urls import reverse
import json

# Importamos las funciones de lógica que queremos probar
from .solver_logic.base_solver import parse_safe, format_latex
from .solver_logic.quadratic_solver import solve_quadratic
from .solver_logic.bernoulli_solver import solve_bernoulli
from .solver_logic.cauchy_euler_solver import solve_cauchy_euler
from .solver_logic.clairaut_solver import solve_clairaut
from .solver_logic.riccati_solver import solve_riccati

# --- Tests para la Lógica Pura (Solvers) ---

class BaseSolverTests(TestCase):
    
    def test_parse_safe_valid(self):
        """Prueba que parse_safe convierte strings válidos."""
        self.assertEqual(str(parse_safe("x**2 + 1")), "x**2 + 1")
        self.assertEqual(str(parse_safe("-5/2*x")), "-5*x/2")
        self.assertEqual(str(parse_safe("3")), "3")

    def test_parse_safe_invalid(self):
        """Prueba que parse_safe rechaza strings inválidos."""
        self.assertIsNone(parse_safe("x + / * y"))
        self.assertIsNone(parse_safe("print('hello')"))
        self.assertIsNone(parse_safe(""))


class QuadraticSolverTests(TestCase):

    def test_solve_quadratic_simple(self):
        """Prueba una ecuación cuadrática simple: x^2 - 1 = 0"""
        # x^2 - 1 = (x-1)(x+1), raíces = [-1, 1]
        result = solve_quadratic("1", "0", "-1")
        self.assertIn('solucion', result)
        self.assertIn(r"\left[ -1, \  1\right]", result['solucion']) # Raíces
        self.assertIn(r"\left(x - 1\right) \left(x + 1\right)", result['solucion']) # Factorizada

    def test_solve_quadratic_invalid_input(self):
        """Prueba una entrada inválida."""
        result = solve_quadratic("1", "b", "c") # 'b' no es un número
        self.assertIn('error', result)
        self.assertIn("'b' no es válido", result['error'])


class BernoulliSolverTests(TestCase):

    def test_solve_bernoulli_pdf_example(self):
        """
        Prueba el ejemplo del PDF: y' - 5y = -5/2*x*y^3
        P(x) = -5, Q(x) = -5/2*x, n = 3
        """
        result = solve_bernoulli("-5", "-5/2*x", "3")
        self.assertIn('solucion', result)
        # La solución es y(x) = ... o y(x)**-2 = ...
        # Verificamos que contenga partes clave
        self.assertIn(r"y^{2}{\left(x \right)} = \frac{1}{C_{1} e^{- 10 x} + \frac{x}{2} - \frac{1}{20}}", result['solucion'])

    def test_solve_bernoulli_invalid_p(self):
        """Prueba una función P(x) inválida."""
        result = solve_bernoulli("1 + / 2", "x", "3")
        self.assertIn('error', result)
        self.assertIn("P(x)", result['error'])

# --- Tests para las Vistas (Integración) ---

class MainSolverViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('main_solver_view') # '/solver/'

    def test_get_request(self):
        """Prueba que la página se carga con un GET."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'math_solver/index.html')
        self.assertContains(response, "Math Solver Pro")

    def test_post_bernoulli_solver(self):
        """Prueba enviar el formulario de Bernoulli."""
        data = {
            'solver_type': 'bernoulli',
            'p_function': '-5',
            'q_function': '-5/2*x',
            'n_value': '3'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'math_solver/index.html')
        
        # Verifica que el contexto de la respuesta contenga la solución
        self.assertIn('context', response.context)
        self.assertIn('solucion', response.context['context'])
        # Verifica que la solución (en HTML) esté presente
        self.assertContains(response, r"y^{2}{\left(x \right)}")

    def test_post_invalid_solver_type(self):
        """Prueba enviar un tipo de solver que no existe."""
        data = {'solver_type': 'non_existent_solver'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('context', response.context)
        self.assertIn('error', response.context['context'])
        self.assertContains(response, "Tipo de solver desconocido")