class HistogramComponent {
    constructor() {
        this.canvas = document.getElementById('monthly-histogram');
        this.chart = null;
        this.data = [];
    }

    async update() {
        try {
            this.data = await API.getMonthlyExpenses();
            this.render(this.data);
        } catch (error) {
            console.error('Failed to load monthly expenses:', error);
            this.clearChart();
        }
    }

    render(data) {
        if (!data || data.length === 0) {
            this.clearChart();
            return;
        }

        this.data = data;
        const component = this;

        const ruMonths = {
            'Jan': 'Янв', 'Feb': 'Фев', 'Mar': 'Мар', 'Apr': 'Апр',
            'May': 'Май', 'Jun': 'Июн', 'Jul': 'Июл', 'Aug': 'Авг',
            'Sep': 'Сен', 'Oct': 'Окт', 'Nov': 'Ноя', 'Dec': 'Дек'
        };

        // Короткие подписи (только месяц) — не выходят за пределы при 9 столбцах
        const labels = data.map(function(item) {
            return ruMonths[item.month] || item.month;
        });
        const values = data.map(function(item) {
            return item.total;
        });
        const colors = data.map(function(item) {
            return item.color;
        });

        if (this.chart) {
            this.chart.data.labels = labels;
            this.chart.data.datasets[0].data = values;
            this.chart.data.datasets[0].backgroundColor = colors;
            this.chart.update();
        } else {
            this.chart = new Chart(this.canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Расходы за месяц',
                        data: values,
                        backgroundColor: colors,
                        hoverBackgroundColor: colors.map(function(c) { return c; }),
                        borderWidth: 0,
                        borderRadius: 12,
                        borderSkipped: false,
                        barPercentage: 0.55,
                        categoryPercentage: 0.85,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    devicePixelRatio: window.devicePixelRatio || 1,
                    onClick: (event, elements) => {
                        if (!elements || elements.length === 0) return;

                        const index = elements[0].index;
                        const item = component.data[index];
                        if (!item) return;

                        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                        const monthIndex = monthNames.indexOf(item.month) + 1;
                        if (monthIndex === 0) return;

                        window.location.href =
                            '/month-detail.html?year=' + item.year + '&month=' + monthIndex;
                    },
                    layout: {
                        // Достаточные боковые отступы, чтобы крайние столбцы
                        // (первый и последний) не обрезались по краям карточки
                        padding: { top: 22, right: 18, bottom: 0, left: 18 }
                    },
                    // Не обрезаем отрисовку у краёв холста
                    clip: false,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            backgroundColor: 'rgba(40,40,50,0.95)',
                            titleColor: '#e2e8f0',
                            bodyColor: '#e2e8f0',
                            bodyFont: { family: 'Segoe UI, Tahoma, sans-serif', weight: 'bold', size: 14 },
                            borderColor: '#3a3a47',
                            borderWidth: 1,
                            cornerRadius: 12,
                            padding: 12,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return 'Расходы: ' + formatCurrency(context.parsed.y);
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            // offset:false выравнивает крайние столбцы внутри области
                            // графика, чтобы они не выходили за пределы по краям
                            offset: false,
                            grid: { display: false },
                            border: { display: false },
                            ticks: {
                                font: { family: 'Segoe UI, Tahoma, sans-serif', size: 11, weight: '600' },
                                color: '#a0aec0',
                                cursor: 'pointer',
                                maxRotation: 0,
                                autoSkip: false,
                            }
                        },
                        y: {
                            // Шкала скрыта (числа 50 000 / 100 000 не показываем),
                            // но используется для масштаба столбцов
                            display: false,
                            beginAtZero: true,
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index',
                    },
                },
                plugins: [{
                    id: 'barValueLabels',
                    afterDatasetsDraw(chart) {
                        const { ctx } = chart;
                        const meta = chart.getDatasetMeta(0);
                        if (!meta.data || meta.data.length === 0) return;

                        ctx.save();
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        ctx.font = 'bold 10px Segoe UI, Tahoma, sans-serif';
                        ctx.fillStyle = '#e2e8f0';
                        ctx.shadowColor = 'rgba(0,0,0,0.5)';
                        ctx.shadowBlur = 3;

                        for (let i = 0; i < meta.data.length; i++) {
                            const bar = meta.data[i];
                            const value = chart.data.datasets[0].data[i];
                            if (value <= 0) continue;
                            // Компактный формат (например «85 тыс»), чтобы не перекрывались при 9 столбцах
                            const thousands = value / 1000;
                            const text = (thousands >= 10 ? Math.round(thousands) : thousands.toFixed(1).replace('.', ',')) + ' тыс';
                            // Прижимаем подпись внутрь холста, чтобы крайние столбцы
                            // (первый/последний) не обрезались по краям
                            const tw = ctx.measureText(text).width;
                            let tx = bar.x;
                            const minX = tw / 2 + 2;
                            const maxX = chart.width - tw / 2 - 2;
                            if (tx < minX) tx = minX;
                            if (tx > maxX) tx = maxX;
                            ctx.fillText(text, tx, bar.y - 5);
                        }
                        ctx.restore();
                    }
                }]
            });
        }
    }

    clearChart() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}