// Enhanced JavaScript for Math Solver Pro with Persistent State
class MathSolverApp {
    constructor() {
        this.init();
    }

    init() {
        this.cacheElements();
        this.initializeState();
        this.bindEvents();
        this.loadInitialSolver();
        this.setupFunctionPalette();
        this.initializeMathJax();
    }

    initializeState() {
        // Initialize state management
        this.solverStates = {}; // Store form data for each solver type
        this.solutionHistory = {}; // Store solutions for each solver type
        this.currentSolver = 'quadratic';
        
        // Load saved state from localStorage
        this.loadStateFromStorage();
    }

    cacheElements() {
        this.solverContent = document.getElementById('solver-content');
        this.solverTypeInput = document.getElementById('solver-type-input');
        this.resultadoBox = document.getElementById('resultado-box');
        this.solverForm = document.getElementById('solver-form');
        this.functionBtns = document.querySelectorAll('.function-btn');
        this.solverNavBtns = document.querySelectorAll('.solver-nav-btn');
        
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
        this.solverForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveCurrentState();
            this.showLoadingState();
            this.submitForm();
        });

        // Function palette buttons
        this.functionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.insertFunction(btn.getAttribute('data-func'));
            });
        });

        // Input change tracking - save state automatically
        document.addEventListener('input', (e) => {
            if (e.target.matches('input[type="text"]')) {
                this.saveCurrentStateDebounced();
            }
        });

        // Input focus tracking for function palette
        document.addEventListener('focusin', (e) => {
            if (e.target.matches('input[type="text"]')) {
                this.currentInput = e.target;
            }
        });

        // Save state before page unload
        window.addEventListener('beforeunload', () => {
            this.saveStateToStorage();
        });

        // Keyboard shortcuts for function palette
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Space to show function palette hint
            if ((e.ctrlKey || e.metaKey) && e.code === 'Space') {
                e.preventDefault();
                this.showFunctionPaletteHint();
            }
            
            // Escape to hide function palette hint
            if (e.code === 'Escape') {
                this.hideFunctionPaletteHint();
            }
        });
    }

    loadStateFromStorage() {
        try {
            const savedState = localStorage.getItem('mathSolverState');
            if (savedState) {
                const state = JSON.parse(savedState);
                this.solverStates = state.solverStates || {};
                this.solutionHistory = state.solutionHistory || {};
                this.currentSolver = state.currentSolver || 'quadratic';
            }
        } catch (e) {
            console.warn('Could not load state from storage:', e);
        }
    }

    saveStateToStorage() {
        try {
            const state = {
                solverStates: this.solverStates,
                solutionHistory: this.solutionHistory,
                currentSolver: this.currentSolver
            };
            localStorage.setItem('mathSolverState', JSON.stringify(state));
        } catch (e) {
            console.warn('Could not save state to storage:', e);
        }
    }

    saveCurrentStateDebounced() {
        clearTimeout(this.saveTimeout);
        this.saveTimeout = setTimeout(() => {
            this.saveCurrentState();
        }, 300);
    }

    saveCurrentState() {
        const formData = new FormData(this.solverForm);
        const state = {};
        
        // Save all form inputs except hidden solver type
        for (let [key, value] of formData.entries()) {
            if (key !== 'solver_type' && key !== 'csrfmiddlewaretoken') {
                state[key] = value;
            }
        }
        
        this.solverStates[this.currentSolver] = state;
        this.saveStateToStorage();
    }

    loadSolverState(solverType) {
        const savedState = this.solverStates[solverType];
        if (savedState) {
            // Restore form values after a short delay to ensure DOM is ready
            setTimeout(() => {
                Object.entries(savedState).forEach(([key, value]) => {
                    const input = document.querySelector(`input[name="${key}"]`);
                    if (input) {
                        input.value = value;
                    }
                });
            }, 100);
        }
    }

    loadSolverSolution(solverType) {
        const savedSolution = this.solutionHistory[solverType];
        if (savedSolution) {
            this.resultadoBox.innerHTML = savedSolution;
            this.rerenderMathJax();
        }
    }

    loadInitialSolver() {
        this.switchSolver(this.currentSolver, false); // Don't clear results on initial load
    }

    switchSolver(solverType, clearResults = true) {
        // Save current state before switching
        this.saveCurrentState();
        
        // Update current solver
        this.currentSolver = solverType;
        this.solverTypeInput.value = solverType;

        // Update navigation UI
        this.updateNavigationUI(solverType);

        // Load solver template
        this.loadSolverTemplate(solverType);

        // Restore saved form data
        this.loadSolverState(solverType);

        // Load saved solution if exists
        if (clearResults) {
            this.clearResults();
        } else {
            this.loadSolverSolution(solverType);
        }

        // Focus first input
        setTimeout(() => {
            const firstInput = this.solverContent.querySelector('input');
            if (firstInput) {
                firstInput.focus();
            }
        }, 150);

        // Force MathJax to re-render after template loads
        this.rerenderMathJax();
        
        // Save state to storage
        this.saveStateToStorage();
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
            this.currentInput.classList.add('ring-2', 'ring-blue-400', 'function-insert-animation');
            setTimeout(() => {
                this.currentInput.classList.remove('ring-2', 'ring-blue-400', 'function-insert-animation');
            }, 500);
            
            // Save state after insertion
            this.saveCurrentStateDebounced();
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

    showLoadingState() {
        const loadingHTML = `
            <div class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-4 text-gray-600">Resolviendo ecuación...</p>
            </div>
        `;
        this.resultadoBox.innerHTML = loadingHTML;
    }

    submitForm() {
        const formData = new FormData(this.solverForm);
        
        // Submit via fetch to avoid page reload
        fetch(this.solverForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data) {
                // Update result box with solution data
                this.updateResultBox(data.data);
                
                // Save solution to history
                this.solutionHistory[this.currentSolver] = this.resultadoBox.innerHTML;
                this.saveStateToStorage();
                
                // Re-render MathJax for new content
                this.rerenderMathJax();
            } else {
                // Handle error case
                this.showError(data.data?.error || 'Unknown error occurred');
            }
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            this.showError(`Error al enviar formulario: ${error.message}`);
        });
    }

    updateResultBox(data) {
        if (data.error) {
            this.showError(data.error);
        } else if (data.solucion) {
            // Generate steps HTML if steps exist
            let stepsHtml = '';
            if (data.steps && data.steps.length > 0) {
                stepsHtml = `
                    <div class="mt-6 pt-4 border-t border-gray-200">
                        <p class="font-bold text-xl mb-4 text-blue-700">Pasos de la Solución:</p>
                        <ol class="list-decimal list-inside space-y-2 text-gray-800">
                            ${data.steps.map(step => `<li>${step}</li>`).join('')}
                        </ol>
                    </div>
                `;
            }
            
            // Render solution with proper formatting
            this.resultadoBox.innerHTML = `
                <div class="p-6 bg-green-50 border border-green-200 rounded-lg">
                    <h3 class="text-lg font-bold text-green-800 mb-4">✅ Solución Encontrada</h3>
                    <div class="text-gray-800">
                        ${data.solucion}
                    </div>
                    ${stepsHtml}
                </div>
            `;
        } else {
            this.showError('No se recibió una solución válida');
        }
    }

    showError(message) {
        this.resultadoBox.innerHTML = `
            <div class="p-4 bg-red-100 border border-red-300 rounded-lg text-red-800">
                <p class="font-bold">❌ Error:</p>
                <p>${message}</p>
            </div>
        `;
    }

    // Force MathJax to re-render all content
    rerenderMathJax() {
        if (window.MathJax) {
            setTimeout(() => {
                window.MathJax.typesetPromise().catch(err => console.error('MathJax render error:', err));
            }, 100);
        }
    }

    showFunctionPaletteHint() {
        // Create or update hint overlay
        let hintOverlay = document.getElementById('function-hint-overlay');
        if (!hintOverlay) {
            hintOverlay = document.createElement('div');
            hintOverlay.id = 'function-hint-overlay';
            hintOverlay.className = 'fixed top-4 right-4 bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-50 max-w-sm';
            document.body.appendChild(hintOverlay);
        }
        
        hintOverlay.innerHTML = `
            <div class="flex justify-between items-center mb-3">
                <h4 class="font-semibold text-gray-800">Atajos de Teclado</h4>
                <button onclick="this.parentElement.parentElement.remove()" class="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <div class="text-sm text-gray-600 space-y-1">
                <p><kbd class="px-2 py-1 bg-gray-100 rounded">Ctrl+Space</kbd> - Mostrar/Ocultar esta ayuda</p>
                <p><kbd class="px-2 py-1 bg-gray-100 rounded">Tab</kbd> - Navegar entre campos</p>
                <p><kbd class="px-2 py-1 bg-gray-100 rounded">Enter</kbd> - Resolver ecuación</p>
                <p><kbd class="px-2 py-1 bg-gray-100 rounded">Escape</kbd> - Cerrar ayuda</p>
            </div>
            <div class="mt-3 pt-3 border-t border-gray-200">
                <p class="text-xs text-gray-500">Haz clic en cualquier función de la paleta para insertarla en el campo activo</p>
            </div>
        `;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (document.getElementById('function-hint-overlay')) {
                hintOverlay.remove();
            }
        }, 5000);
    }

    hideFunctionPaletteHint() {
        const hintOverlay = document.getElementById('function-hint-overlay');
        if (hintOverlay) {
            hintOverlay.remove();
        }
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
    },
    
    clearAllData: () => {
        if (confirm('¿Estás seguro de que quieres borrar todos los datos guardados?')) {
            localStorage.removeItem('mathSolverState');
            location.reload();
        }
    }
};