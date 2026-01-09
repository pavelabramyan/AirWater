let profitChart = null;

function updateChart(period, annualProfit, realInvestment) {
    const ctx = document.getElementById('profitChart');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (profitChart) {
        profitChart.destroy();
    }
    
    // Prepare data
    const years = [];
    const cumulativeProfit = [];
    const cumulativeInvestment = [];
    let totalProfit = 0;
    
    for (let year = 1; year <= period; year++) {
        years.push(year);
        totalProfit += annualProfit;
        cumulativeProfit.push(totalProfit);
        cumulativeInvestment.push(realInvestment);
    }
    
    // Create chart using Chart.js (we'll use a simple canvas implementation)
    profitChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years.map(y => `Year ${y}`),
            datasets: [
                {
                    label: 'Cumulative Profit',
                    data: cumulativeProfit,
                    borderColor: '#0066cc',
                    backgroundColor: 'rgba(0, 102, 204, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                },
                {
                    label: 'Investment',
                    data: cumulativeInvestment,
                    borderColor: '#00b8d4',
                    backgroundColor: 'rgba(0, 184, 212, 0.1)',
                    fill: true,
                    tension: 0,
                    borderWidth: 2,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            family: 'Inter'
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatCurrency(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) {
                                return '$' + (value / 1000000).toFixed(1) + 'M';
                            }
                            return '$' + (value / 1000).toFixed(0) + 'K';
                        },
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Chart.js is loaded in HTML head, so we can use it directly
// Initialize chart when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Chart will be created when calculateROI is called
});

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}
