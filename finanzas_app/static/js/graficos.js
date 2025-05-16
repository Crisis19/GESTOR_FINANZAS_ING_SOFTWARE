document.addEventListener('DOMContentLoaded', () => {
    // Verificar si Chart.js está disponible
    if (typeof Chart === 'undefined') {
        console.error('Chart.js no está cargado.');
        return;
    }

    // Obtener datos del servidor
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
                            display: true,
                            text: 'Distribución de Gastos por Categoría',
                            font: {
                                size: 18
                            }
                        },
                        legend: {
                            position: 'top',
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
                            text: 'Ingresos vs Gastos Mensuales',
                            font: {
                                size: 18
                            }
                        },
                        legend: {
                            display: false // Ocultar leyenda si no es necesaria
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