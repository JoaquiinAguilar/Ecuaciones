#!/usr/bin/env python3

# Test script for enhanced Riccati solver
import sys
import os

# Add the project path to sys.path
sys.path.insert(0, '/home/joaquin/Desktop/Ecuaciones/math_project')

# Mock sympy imports for testing structure
class MockSymbol:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Symbol('{self.name}')"
    def has(self, other):
        return False
    @property
    def is_number(self):
        return True
    def is_polynomial(self, other):
        return True

class MockFunction:
    def __init__(self, name):
        self.name = name
    def __call__(self, *args):
        return MockExpr(f"{self.name}({', '.join(str(arg) for arg in args)})")
    def diff(self, *args):
        return MockExpr(f"diff({self.name}, {', '.join(str(arg) for arg in args)})")

class MockExpr:
    def __init__(self, expr_str):
        self.expr_str = expr_str
    def __str__(self):
        return self.expr_str
    def __repr__(self):
        return f"Expr({self.expr_str})"
    def has(self, other):
        return False
    @property
    def is_number(self):
        return True
    def is_polynomial(self, other):
        return True

# Mock sympy module
import types
sympy_mock = types.ModuleType('sympy')
sympy_mock.Eq = lambda a, b: MockExpr(f"Eq({a}, {b})")
sympy_mock.dsolve = lambda eq, y=None: MockExpr(f"Solution({eq})")
sympy_mock.latex = lambda expr: str(expr)
sympy_mock.symbols = MockSymbol
sympy_mock.Function = MockFunction
sympy_mock.diff = lambda f, x: MockExpr(f"diff({f}, {x})")
sympy_mock.simplify = lambda expr: expr
sympy_mock.integrate = lambda expr, var: MockExpr(f"integrate({expr}, {var})")
sympy_mock.exp = lambda expr: MockExpr(f"exp({expr})")
sympy_mock.log = lambda expr: MockExpr(f"log({expr})")
sympy_mock.solve = lambda eq, var: [MockSymbol("C1")]
sympy_mock.Rational = lambda a, b: MockExpr(f"{a}/{b}")
sympy_mock.sqrt = lambda expr: MockExpr(f"sqrt({expr})")
sympy_mock.atan = lambda expr: MockExpr(f"atan({expr})")
sympy_mock.asin = lambda expr: MockExpr(f"asin({expr})")
sympy_mock.acos = lambda expr: MockExpr(f"acos({expr})")
sympy_mock.tan = lambda expr: MockExpr(f"tan({expr})")
sympy_mock.sin = lambda expr: MockExpr(f"sin({expr})")
sympy_mock.cos = lambda expr: MockExpr(f"cos({expr})")
sympy_mock.airyai = lambda expr: MockExpr(f"airyai({expr})")
sympy_mock.airybi = lambda expr: MockExpr(f"airybi({expr})")
sympy_mock.besselj = lambda nu, expr: MockExpr(f"besselj({nu}, {expr})")
sympy_mock.bessely = lambda nu, expr: MockExpr(f"bessely({nu}, {expr})")
sympy_mock.hyper = lambda *args: MockExpr(f"hyper({', '.join(str(arg) for arg in args)})")
sympy_mock.meijerg = lambda *args: MockExpr(f"meijerg({', '.join(str(arg) for arg in args)})")
sympy_mock.classify_ode = lambda eq: ['riccati', 'lie_group']
sympy_mock.odesimp = lambda sol: sol
sympy_mock.checkodesol = lambda eq, sol: True

sys.modules['sympy'] = sympy_mock

# Mock base_solver
base_solver_mock = types.ModuleType('base_solver')
base_solver_mock.x = MockSymbol('x')
base_solver_mock.y = MockFunction('y')(MockSymbol('x'))
base_solver_mock.parse_safe = lambda s: MockExpr(s) if s else None
base_solver_mock.format_latex = lambda expr: str(expr)

sys.modules['math_solver.solver_logic.base_solver'] = base_solver_mock

# Now test our enhanced solver
try:
    from math_solver.solver_logic.riccati_solver import solve_riccati
    
    print("Testing Enhanced Riccati Solver")
    print("=" * 50)
    
    # Test case 1: Simple separable case
    print("\nTest 1: Separable case y' = y^2")
    result = solve_riccati("1", "0", "0")
    print(f"Result type: {type(result)}")
    if 'solucion' in result:
        print(f"Solution: {result['solucion']}")
    if 'steps' in result:
        print(f"Number of steps: {len(result['steps'])}")
        print("First few steps:")
        for i, step in enumerate(result['steps'][:5]):
            print(f"  {i+1}. {step}")
    
    # Test case 2: Linear case
    print("\nTest 2: Linear case y' = 2y + 3")
    result = solve_riccati("0", "2", "3")
    if 'solucion' in result:
        print(f"Solution: {result['solucion']}")
    
    # Test case 3: Constant coefficients
    print("\nTest 3: Constant coefficients y' = y^2 + 2y + 1")
    result = solve_riccati("1", "2", "1")
    if 'solucion' in result:
        print(f"Solution: {result['solucion']}")
    
    print("\n" + "=" * 50)
    print("Enhanced Riccati solver test completed successfully!")
    
except Exception as e:
    print(f"Error testing solver: {e}")
    import traceback
    traceback.print_exc()