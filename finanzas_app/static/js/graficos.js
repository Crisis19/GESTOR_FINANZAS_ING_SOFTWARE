// Obtener datos del servidor
document.addEventListener('DOMContentLoaded', () => {
console.log(typeof Chart);
fetch('/graficos/')
    .then(response => response.json())
    .then(data => {
        // Gráfica de pastel: Distribución de gastos por categoría
        const ctxPastel = document.getElementById('graficoPastel').getContext('2d');
        const categorias = data.gastos_por_categoria.map(item => item.categoria__nombre);
        const montos = data.gastos_por_categoria.map(item => item.total);

        new Chart(ctxPastel, {
            type: 'pie',
            data: {
                labels: categorias,
                datasets: [{
                    label: 'Gastos por Categoría',
                    data: montos,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true, // Muestra el título
                        text: 'Distribución de Gastos por Categoría', // Texto del título
                        font: {
                            size: 18 // Tamaño de la fuente
                        }
                    }
                }
            }
        });

        // Gráfica de barras: Ingresos vs Gastos
        const ctxBarras = document.getElementById('graficoBarras').getContext('2d');
        new Chart(ctxBarras, {
            type: 'bar',
            data: {
                labels: ['Ingresos', 'Gastos'],
                datasets: [{
                    label: 'Comparación Ingresos vs Gastos',
                    data: [data.ingresos, data.gastos],
                    backgroundColor: ['#4CAF50', '#F44336'],
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Comparación de Ingresos y Gastos',
                        font: {
                            size: 18
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error al cargar los datos:', error));
});