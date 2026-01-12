let profitChart = null;

// Получаем локализованные названия для графика
function getChartLabels() {
    const lang = window.currentLang || 'ru';
    
    const labels = {
        ru: {
            cumulativeProfit: 'Накопленная прибыль',
            investment: 'Инвестиции',
            breakeven: 'Точка безубыточности',
            year: 'Год',
            days: 'Дней до безубыточности',
            payback: 'Окупаемость'
        },
        en: {
            cumulativeProfit: 'Cumulative Profit',
            investment: 'Investment',
            breakeven: 'Break-even Point',
            year: 'Year',
            days: 'Days to break-even',
            payback: 'Payback'
        },
        zh: {
            cumulativeProfit: '累计利润',
            investment: '投资',
            breakeven: '盈亏平衡点',
            year: '年',
            days: '收支平衡天数',
            payback: '回收期'
        },
        es: {
            cumulativeProfit: 'Ganancia Acumulada',
            investment: 'Inversión',
            breakeven: 'Punto de Equilibrio',
            year: 'Año',
            days: 'Días hasta equilibrio',
            payback: 'Recuperación'
        }
    };
    
    return labels[lang] || labels.ru;
}

function updateBreakevenChart(investment, annualProfit, period, breakevenDays) {
    const ctx = document.getElementById('profitChart');
    if (!ctx) return;
    
    // Уничтожаем существующий график
    if (profitChart) {
        profitChart.destroy();
    }
    
    const labels = getChartLabels();
    
    // Подготовка данных по месяцам для первых 3 лет, затем по годам
    const dataPoints = [];
    const cumulativeProfit = [];
    const investmentLine = [];
    
    let totalProfit = 0;
    const monthlyProfit = annualProfit / 12;
    
    // Первые 36 месяцев помесячно
    for (let month = 1; month <= Math.min(36, period * 12); month++) {
        totalProfit += monthlyProfit;
        dataPoints.push(month);
        cumulativeProfit.push(totalProfit);
        investmentLine.push(investment);
    }
    
    // Если период больше 3 лет, добавляем остаток погодам
    if (period > 3) {
        for (let year = 4; year <= period; year++) {
            totalProfit += annualProfit;
            dataPoints.push(36 + (year - 3) * 12);
            cumulativeProfit.push(totalProfit);
            investmentLine.push(investment);
        }
    }
    
    // Находим точку пересечения (окупаемость)
    let breakevenIndex = -1;
    for (let i = 0; i < cumulativeProfit.length; i++) {
        if (cumulativeProfit[i] >= investment) {
            breakevenIndex = i;
            break;
        }
    }
    
    // Создаём метки
    const xLabels = dataPoints.map(m => {
        if (m <= 12) return m + ' ' + getMonthLabel(m);
        if (m <= 36) return Math.floor(m / 12) + ' ' + labels.year + ' ' + (m % 12 || 12) + ' м.';
        return Math.floor(m / 12) + ' ' + labels.year;
    });
    
    // Аннотация для точки безубыточности
    const annotations = {};
    if (breakevenIndex >= 0) {
        annotations.breakeven = {
            type: 'line',
            xMin: breakevenIndex,
            xMax: breakevenIndex,
            borderColor: '#ff6b6b',
            borderWidth: 2,
            borderDash: [6, 6],
            label: {
                display: true,
                content: labels.breakeven,
                position: 'start',
                backgroundColor: '#ff6b6b',
                color: '#fff',
                font: { size: 11, family: 'Inter' }
            }
        };
    }
    
    // Создаём график
    profitChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: labels.cumulativeProfit,
                    data: cumulativeProfit,
                    borderColor: '#00b894',
                    backgroundColor: 'rgba(0, 184, 148, 0.1)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3,
                    pointRadius: 0,
                    pointHoverRadius: 6
                },
                {
                    label: labels.investment,
                    data: investmentLine,
                    borderColor: '#0984e3',
                    backgroundColor: 'rgba(9, 132, 227, 0.05)',
                    fill: true,
                    tension: 0,
                    borderWidth: 2,
                    borderDash: [8, 4],
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: { size: 13, family: 'Inter', weight: '500' },
                        padding: 16,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleFont: { size: 13, family: 'Inter' },
                    bodyFont: { size: 12, family: 'Inter' },
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatCurrencyChart(context.parsed.y);
                        }
                    }
                },
                annotation: {
                    annotations: annotations
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
                            if (value >= 1000) {
                                return '$' + (value / 1000).toFixed(0) + 'K';
                            }
                            return '$' + value;
                        },
                        font: { size: 11, family: 'Inter' },
                        maxTicksLimit: 8
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.04)'
                    }
                },
                x: {
                    ticks: {
                        font: { size: 10, family: 'Inter' },
                        maxRotation: 45,
                        minRotation: 0,
                        maxTicksLimit: 12
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function getMonthLabel(month) {
    const lang = window.currentLang || 'ru';
    const labels = {
        ru: 'мес.',
        en: 'mo.',
        zh: '月',
        es: 'mes'
    };
    return labels[lang] || labels.ru;
}

function formatCurrencyChart(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    // График будет создан при вызове calculateROI
});
