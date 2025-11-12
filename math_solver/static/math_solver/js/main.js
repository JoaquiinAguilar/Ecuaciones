// Enhanced JavaScript for Math Solver Pro
class MathSolverApp {
    constructor() {
        this.init();
    }

    init() {
        this.cacheElements();
        this.bindEvents();
        this.loadInitialSolver();
        this.setupFunctionPalette();
        this.initializeMathJax();
    }

    cacheElements() {
        this.solverContent = document.getElementById('solver-content');
        this.solverTypeInput = document.getElementById('solver-type-input');
        this.resultadoBox = document.getElementById('resultado-box');
        this.solverForm = document.getElementById('solver-form');
        this.functionBtns = document.querySelectorAll('.function-btn');
        this.solverNavBtns = document.querySelectorAll('.solver-nav-btn');
        
        // Debug: Check if elements exist
        console.log('Elements found:', {
            solverContent: !!this.solverContent,
            solverTypeInput: !!this.solverTypeInput,
            resultadoBox: !!this.resultadoBox,
            solverForm: !!this.solverForm,
            functionBtns: this.functionBtns.length,
            solverNavBtns: this.solverNavBtns.length
        });
        
        // Check if templates exist
        const templateIds = ['template-quadratic', 'template-bernoulli', 'template-cauchy', 'template-clairaut', 'template-riccati', 'template-second_order_homogeneous', 'template-second_order_nonhomogeneous'];
        templateIds.forEach(id => {
            const template = document.getElementById(id);
            console.log(`Template ${id}:`, !!template);
        });
        
        // Store placeholder HTML
        this.resultadoPlaceholderHTML = document.getElementById('resultado-placeholder')?.outerHTML || 
            '<div class="text-center text-gray-500 pt-16"><svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg><p class="text-lg font-medium">Tu solución aparecerá aquí...</p><p class="text-sm mt-2">Selecciona un tipo de ecuación y completa los parámetros</p></div>';
    }

    bindEvents() {
        // Navigation buttons
        this.solverNavBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const solverType = btn.getAttribute('data-solver');
                this.switchSolver(solverType);
            });
        });

        // Form submission
        this.solverForm.addEventListener('submit', () => {
            this.showLoadingState();
        });

        // Function palette buttons
        this.functionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.insertFunction(btn.getAttribute('data-func'));
            });
        });

        // Input focus tracking for function palette
        document.addEventListener('focusin', (e) => {
            if (e.target.matches('input[type="text"]')) {
                this.currentInput = e.target;
            }
        });
    }

    loadInitialSolver() {
        const initialSolver = window.djangoContext?.lastSolver || 'quadratic';
        console.log('Loading initial solver:', initialSolver);
        
        // Wait a bit for DOM to be ready
        setTimeout(() => {
            this.switchSolver(initialSolver, false); // Don't clear results on initial load
        }, 100);
    }

    switchSolver(solverType, clearResults = true) {
        console.log('Switching to solver:', solverType);
        
        // Update hidden input
        this.solverTypeInput.value = solverType;

        // Update navigation UI
        this.updateNavigationUI(solverType);

        // Load solver template
        this.loadSolverTemplate(solverType);

        // Clear results if requested
        if (clearResults) {
            this.clearResults();
        }

        // Focus first input
        setTimeout(() => {
            const firstInput = this.solverContent.querySelector('input');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);

        // Force MathJax to re-render after template loads
        this.rerenderMathJax();
    }

    updateNavigationUI(solverType) {
        // Remove active class from all buttons
        this.solverNavBtns.forEach(btn => {
            btn.classList.remove('bg-blue-100', 'border-blue-400', 'bg-green-100', 'border-green-400');
        });

        // Add active class to selected button
        const activeBtn = document.querySelector(`[data-solver="${solverType}"]`);
        if (activeBtn) {
            const isSecondOrder = solverType.includes('second_order');
            activeBtn.classList.add(
                isSecondOrder ? 'bg-green-100' : 'bg-blue-100',
                isSecondOrder ? 'border-green-400' : 'border-blue-400'
            );
        }
    }

    loadSolverTemplate(solverType) {
        const template = document.getElementById(`template-${solverType}`);
        console.log('Loading template:', `template-${solverType}`, 'Found:', !!template);
        
        if (template) {
            // Clone template content
            const content = template.content.cloneNode(true);
            
            // Clear current content and append new
            this.solverContent.innerHTML = '';
            this.solverContent.appendChild(content);

            // Add input animations
            this.animateInputs();

            // Force MathJax to re-render after template is loaded
            setTimeout(() => {
                this.rerenderMathJax();
            }, 50);
        } else {
            console.log(`Using fallback template for: ${solverType}`);
            // Use JavaScript fallback template
            this.solverContent.innerHTML = solverTemplates[solverType] || `
                <div class="p-4 bg-red-100 border border-red-300 rounded-lg text-red-800">
                    <p class="font-bold">Error:</p>
                    <p>No se encontró la plantilla para: ${solverType}</p>
                </div>
            `;

            // Add input animations
            this.animateInputs();

            // Force MathJax to re-render after template is loaded
            setTimeout(() => {
                this.rerenderMathJax();
            }, 50);
        }
    }

    animateInputs() {
        const inputs = this.solverContent.querySelectorAll('input');
        inputs.forEach((input, index) => {
            input.style.opacity = '0';
            input.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                input.style.transition = 'all 0.3s ease';
                input.style.opacity = '1';
                input.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    setupFunctionPalette() {
        // Add keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 's':
                        e.preventDefault();
                        this.insertFunction('sin(x)');
                        break;
                    case 'c':
                        e.preventDefault();
                        this.insertFunction('cos(x)');
                        break;
                    case 'l':
                        e.preventDefault();
                        this.insertFunction('log(x)');
                        break;
                    case 'e':
                        e.preventDefault();
                        this.insertFunction('exp(x)');
                        break;
                }
            }
        });
    }

    insertFunction(funcText) {
        if (!this.currentInput) {
            // If no input is focused, focus the first visible input
            this.currentInput = this.solverContent.querySelector('input:not([type="hidden"])');
        }

        if (this.currentInput) {
            const start = this.currentInput.selectionStart;
            const end = this.currentInput.selectionEnd;
            const currentValue = this.currentInput.value;
            
            // Insert the function at cursor position
            this.currentInput.value = currentValue.substring(0, start) + funcText + currentValue.substring(end);
            this.currentInput.selectionStart = this.currentInput.selectionEnd = start + funcText.length;
            this.currentInput.focus();

            // Add visual feedback
            this.currentInput.classList.add('ring-2', 'ring-blue-400');
            setTimeout(() => {
                this.currentInput.classList.remove('ring-2', 'ring-blue-400');
            }, 500);
        }
    }

    clearResults() {
        this.resultadoBox.innerHTML = this.resultadoPlaceholderHTML;
        
        // Re-render MathJax if necessary
        if (window.MathJax) {
            window.MathJax.typesetClear([this.resultadoBox]);
            window.MathJax.typesetPromise([this.resultadoBox]).catch(err => console.error(err));
        }
    }

    // Force MathJax to re-render all content
    rerenderMathJax() {
        if (window.MathJax) {
            setTimeout(() => {
                window.MathJax.typesetPromise().catch(err => console.error('MathJax render error:', err));
            }, 100);
        }
    }

    showLoadingState() {
        const loadingHTML = `
            <div class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-4 text-gray-600">Resolviendo ecuación...</p>
            </div>
        `;
        this.resultadoBox.innerHTML = loadingHTML;
    }

    // Public method to handle server responses
    handleServerResponse(hasSolution, hasError) {
        if (hasSolution || hasError) {
            // Re-render MathJax for new content
            if (window.MathJax) {
                setTimeout(() => {
                    window.MathJax.typesetPromise([this.resultadoBox]).catch(err => console.error('Error al renderizar MathJax:', err));
                }, 100);
            }
        }
    }

    // Initialize MathJax on page load
    initializeMathJax() {
        if (window.MathJax) {
            // Configure MathJax for better rendering
            window.MathJax = {
                tex: {
                    inlineMath: [['\\(', '\\)']],
                    displayMath: [['$$', '$$']],
                    processEscapes: true
                },
                startup: {
                    typeset: false
                }
            };
            
            // Force initial render
            setTimeout(() => {
                this.rerenderMathJax();
            }, 200);
        }
    }
}

// Template fallbacks in case HTML templates don't work
const solverTemplates = {
    quadratic: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Ecuación Cuadrática</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( ax^2 + bx + c = 0 \\)</p>
            <div class="space-y-4">
                <input type="text" name="quad_a_val" placeholder="Coeficiente 'a'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="quad_b_val" placeholder="Coeficiente 'b'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="quad_c_val" placeholder="Coeficiente 'c'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-blue-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Resolver Ecuación Cuadrática
            </button>
        </div>
    `,
    bernoulli: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Ecuación de Bernoulli</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( y' + P(x)y = Q(x)y^n \\)</p>
            <div class="space-y-4">
                <input type="text" name="bernoulli_p_function" placeholder="Función P(x), ej: -5" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="bernoulli_q_function" placeholder="Función Q(x), ej: -5/2*x" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="bernoulli_n_value" placeholder="Exponente 'n', ej: 3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-blue-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Resolver Bernoulli
            </button>
        </div>
    `,
    cauchy: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Ecuación de Cauchy-Euler</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( ax^2y'' + bxy' + cy = R(x) \\)</p>
            <div class="space-y-4">
                <input type="text" name="cauchy_a_val" placeholder="Coeficiente 'a'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="cauchy_b_val" placeholder="Coeficiente 'b'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="cauchy_c_val" placeholder="Coeficiente 'c'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="cauchy_r_function" placeholder="Función R(x), ej: 0" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-blue-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Resolver Cauchy-Euler
            </button>
        </div>
    `,
    clairaut: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Ecuación de Clairaut</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( y = xy' + f(y') \\)</p>
            <p class="text-sm text-gray-600 mb-4">Use 'p' para representar \\( y' \\). Ej: \\( p**2 \\)</p>
            <div class="space-y-4">
                <input type="text" name="clairaut_f_p_function" placeholder="Función f(p), ej: p**2 + 1" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-blue-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Resolver Clairaut
            </button>
        </div>
    `,
    riccati: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Ecuación de Riccati</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( y' = P(x)y^2 + Q(x)y + R(x) \\)</p>
            <div class="space-y-4">
                <input type="text" name="riccati_p_function" placeholder="Función P(x), ej: 1" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="riccati_q_function" placeholder="Función Q(x), ej: 2/x" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" name="riccati_r_function" placeholder="Función R(x), ej: -1/x**2" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-blue-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Resolver Riccati
            </button>
        </div>
    `,
    second_order_homogeneous: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Segundo Orden Homogéneo</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( ay'' + by' + cy = 0 \\)</p>
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                <p class="text-sm text-green-800">
                    <strong>Tipos de soluciones:</strong><br>
                    • Raíces reales distintas: \\( y = C_1e^{r_1x} + C_2e^{r_2x} \\)<br>
                    • Raíz real doble: \\( y = (C_1 + C_2x)e^{rx} \\)<br>
                    • Raíces complejas: \\( y = e^{\\alpha x}(C_1\\cos(\\beta x) + C_2\\sin(\\beta x)) \\)
                </p>
            </div>
            <div class="space-y-4">
                <input type="text" name="second_a_val" placeholder="Coeficiente 'a'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                <input type="text" name="second_b_val" placeholder="Coeficiente 'b'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                <input type="text" name="second_c_val" placeholder="Coeficiente 'c'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
            </div>
            <button type="submit" class="w-full bg-green-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-green-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
                Resolver Segundo Orden Homogéneo
            </button>
        </div>
    `,
    second_order_nonhomogeneous: `
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800">Segundo Orden No Homogéneo</h3>
            <p class="text-gray-700 mb-4">Resuelve: \\( ay'' + by' + cy = g(x) \\)</p>
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                <p class="text-sm text-green-800">
                    <strong>Método de solución:</strong><br>
                    • Resolver ecuación homogénea asociada<br>
                    • Encontrar solución particular<br>
                    • Solución general: \\( y = y_h + y_p \\)
                </p>
            </div>
            <div class="space-y-4">
                <input type="text" name="second_a_val" placeholder="Coeficiente 'a'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                <input type="text" name="second_b_val" placeholder="Coeficiente 'b'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                <input type="text" name="second_c_val" placeholder="Coeficiente 'c'" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
                <input type="text" name="second_g_function" placeholder="Función g(x), ej: exp(x)" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" required>
            </div>
            <button type="submit" class="w-full bg-green-600 text-white font-bold py-3 px-6 rounded-lg mt-6 hover:bg-green-700 transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
                Resolver Segundo Orden No Homogéneo
            </button>
        </div>
    `
};

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.mathSolverApp = new MathSolverApp();
    
    // Handle server-side rendering
    if (window.djangoContext) {
        window.mathSolverApp.handleServerResponse(
            window.djangoContext.hasSolution,
            window.djangoContext.hasError
        );
    }
});

// Add some utility functions
window.MathSolverUtils = {
    formatNumber: (num) => {
        return parseFloat(num).toFixed(6).replace(/\.?0+$/, '');
    },
    
    copyToClipboard: (text) => {
        navigator.clipboard.writeText(text).then(() => {
            // Show toast notification
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
            toast.textContent = '¡Copiado al portapapeles!';
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 2000);
        });
    }
};