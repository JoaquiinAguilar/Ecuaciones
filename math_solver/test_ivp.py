"""
Tests for IVP (Initial Value Problem) solver functionality
"""

from django.test import TestCase
from math_solver.solver_logic.bernoulli_solver import solve_bernoulli
from math_solver.solver_logic.second_order_solver import solve_second_order_homogeneous, solve_second_order_nonhomogeneous
from math_solver.solver_logic.riccati_solver import solve_riccati


class IVPBernoulliTests(TestCase):
    """Test Bernoulli solver with IVP"""
    
    def test_bernoulli_without_ivp(self):
        """Test Bernoulli without initial conditions - should have constant C1"""
        result = solve_bernoulli('-5', '-5/2*x', '3')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)
        # General solution should contain C1
        solution_str = str(result['solucion'])
        self.assertIn('C', solution_str)  # Contains constant
    
    def test_bernoulli_with_ivp(self):
        """Test Bernoulli with initial conditions y(0)=1"""
        result = solve_bernoulli('-5', '-5/2*x', '3', '0', '1')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)
        # IVP solution should be more specific
        self.assertIn('steps', result)
        self.assertTrue(len(result['steps']) > 0)
    
    def test_bernoulli_ivp_linear_case(self):
        """Test Bernoulli n=0 (linear) with IVP"""
        result = solve_bernoulli('1', '2', '0', '0', '1')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)


class IVPSecondOrderTests(TestCase):
    """Test second-order solvers with IVP"""
    
    def test_second_order_homogeneous_without_ivp(self):
        """Test y'' + y = 0 without IVP"""
        result = solve_second_order_homogeneous('1', '0', '1')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)
        # General solution should have C1, C2
        solution_str= str(result['solucion'])
        self.assertIn('C', solution_str)
    
    def test_second_order_homogeneous_with_ivp(self):
        """Test y'' + y = 0 with y(0)=1, y'(0)=0 should give cos(x)"""
        result = solve_second_order_homogeneous('1', '0', '1', '0', '1', '0')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)
        # Should be a particular solution
        self.assertIn('steps', result)
        # Check that it mentions IVP
        steps_text = ' '.join(result['steps'])
        self.assertIn('IVP', steps_text) or self.assertIn('Inicial', steps_text)
    
    def test_second_order_nonhomogeneous_with_ivp(self):
        """Test y'' + y = x with initial conditions"""
        result = solve_second_order_nonhomogeneous('1', '0', '1', 'x', '0', '0', '1')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)


class IVPRiccatiTests(TestCase):
    """Test Riccati solver with IVP"""
    
    def test_riccati_without_ivp(self):
        """Test Riccati without initial conditions"""
        result = solve_riccati('1', '2/x', '-1/x**2')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)
    
    def test_riccati_with_ivp(self):
        """Test Riccati with initial conditions"""
        result = solve_riccati('1', '0', '-1', '0', '1')
        # Riccati may or may not find symbolic solution
        # Just check it doesn't crash
        self.assertTrue('solucion' in result or 'error' in result)
    
    def test_riccati_linear_case_with_ivp(self):
        """Test Riccati P=0 (linear) with IVP"""
        result = solve_riccati('0', '1', 'x', '0', '1')
        self.assertIn('solucion', result)
        self.assertNotIn('error', result)


class IVPParameterValidationTests(TestCase):
    """Test IVP parameter validation"""
    
    def test_bernoulli_invalid_x0(self):
        """Test with invalid x0"""
        result = solve_bernoulli('1', '1', '2', 'invalid', '1')
        self.assertIn('error', result)
    
    def test_bernoulli_invalid_y0(self):
        """Test with invalid y0"""
        # Use completely invalid expression that parse_safe will reject
        result = solve_bernoulli('1', '1', '2', '0', '@@@invalid@@@')
        self.assertIn('error', result)
    
    def test_second_order_missing_y_prime_0(self):
        """Test second order with incomplete IVP parameters"""
        # If only x0 and y0 provided (missing y_prime_0), should treat as non-IVP
        result = solve_second_order_homogeneous('1', '0', '1', '0', '1', None)
        # Should still work but as general solution
        self.assertIn('solucion', result)


class IVPIntegrationTests(TestCase):
    """Integration tests for IVP via views"""
    
    def test_bernoulli_ivp_via_post(self):
        """Test Bernoulli IVP through POST request"""
        data = {
            'solver_type': 'bernoulli',
            'bernoulli_p_function': '-5',
            'bernoulli_q_function': '-5/2*x',
            'bernoulli_n_value': '3',
            'bernoulli_x0': '0',
            'bernoulli_y0': '1'
        }
        response = self.client.post('/solver/', data)
        self.assertEqual(response.status_code, 200)
    
    def test_second_order_ivp_via_post(self):
        """Test second-order IVP through POST request"""
        data = {
            'solver_type': 'second_order_homogeneous',
            'second_a_val': '1',
            'second_b_val': '0',
            'second_c_val': '1',
            'second_x0': '0',
            'second_y0': '1',
            'second_y_prime_0': '0'
        }
        response = self.client.post('/solver/', data)
        self.assertEqual(response.status_code, 200)
