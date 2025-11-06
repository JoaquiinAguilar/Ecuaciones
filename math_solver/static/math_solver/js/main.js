// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Referencias a elementos del DOM ---
    const tabsContainer = document.getElementById('tabs');
    const tabs = tabsContainer.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const solverTypeInput = document.getElementById('solver-type-input');
    
    // --- NUEVA FUNCIÓN: Referencias al área de resultado ---
    const resultadoBox = document.getElementById('resultado-box');
    // Guardamos el HTML del placeholder para reusarlo
    const resultadoPlaceholderHTML = document.getElementById('resultado-placeholder')?.outerHTML || '<div class="text-center text-gray-500 pt-16"><p>Tu solución aparecerá aquí...</p></div>';

    // --- 2. Función para cambiar de Pestaña ---
    function switchTab(tabId) {
        // Actualizar el input oculto
        solverTypeInput.value = tabId;

        // Actualizar clases 'active' en botones de pestaña
        tabs.forEach(t => {
            if (t.getAttribute('data-tab') === tabId) {
                t.classList.add('active');
            } else {
                t.classList.remove('active');
            }
        });

        // Actualizar clases 'active' en contenido de pestaña
        tabContents.forEach(c => {
            if (c.id === 'tab-' + tabId) {
                c.classList.add('active');
            } else {
                c.classList.remove('active');
            }
        });
    }

    // --- 3. Añadir Event Listeners a los botones ---
    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = tab.getAttribute('data-tab');
            switchTab(tabId);
            
            // --- NUEVA FUNCIÓN: Limpiar el resultado ---
            // Cuando un usuario hace clic en una pestaña,
            // reseteamos el cuadro de resultado.
            resultadoBox.innerHTML = resultadoPlaceholderHTML;
            
            // Re-renderizar MathJax si es necesario (aunque el placeholder no tiene)
            if (window.MathJax) {
                window.MathJax.typesetClear([resultadoBox]);
                window.MathJax.typesetPromise([resultadoBox]).catch(err => console.error(err));
            }
        });
    });

    // --- 4. Activar la Pestaña Correcta al Cargar la Página ---
    // 'last_solver' viene del contexto de Django: {{ context.last_solver }}
    // Esto asegura que si la página se recarga (ej. después de un POST),
    // se muestre la pestaña correcta.
    const initialTabId = solverTypeInput.value || 'quadratic';
    
    // Activar la pestaña inicial sin limpiar el resultado
    // (porque el resultado puede ser la solución que acabamos de calcular)
    solverTypeInput.value = initialTabId;

    tabs.forEach(t => {
        if (t.getAttribute('data-tab') === initialTabId) {
            t.classList.add('active');
        } else {
            t.classList.remove('active');
        }
    });

    tabContents.forEach(c => {
        if (c.id === 'tab-' + initialTabId) {
            c.classList.add('active');
        } else {
            c.classList.remove('active');
        }
    });
    
    // --- 5. Renderizar MathJax en el resultado inicial ---
    // (Si la página se cargó con una solución)
    if (window.MathJax && (window.djangoContext.hasSolution || window.djangoContext.hasError)) {
        // Retrasar ligeramente MathJax para asegurar que el DOM esté listo
        setTimeout(() => {
            window.MathJax.typesetPromise([resultadoBox]).catch(err => console.error('Error al renderizar MathJax:', err));
        }, 100); // 100ms de retraso
    }
});