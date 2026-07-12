class HistogramComponent {
    constructor() {
        this.canvas = document.getElementById('monthly-histogram');
        this.chart = null;
        this.data = [];
    }
    async update() {
        try {
            this.data = await API.getMonthlyExpenses();
            console.log('Monthly expenses:', this.data);
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
        const labels = data.map(function(item) {
            return item.month + ' ' + item.year;
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
                        borderColor: colors.map(function(c) { return c; }),
                        borderWidth: 2,
                        borderRadius: 8,
                        barPercentage: 0.7,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    onClick: function(event, elements) {
                        if (elements && elements.length > 0) {
                            const index = elements[0].index;
                            const item = this.data.datasets[0].data[index];
                            const label = this.data.labels[index];
                            const parts = label.split(' ');
                            const month = parts[0];
                            const year = parseInt(parts[1]);
                            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                            const monthIndex = monthNames.indexOf(month) + 1;
                            window.location.href = '/month-detail.html?year=' + year + '&month=' + monthIndex;
                        }
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            backgroundColor: 'rgba(255,255,255,0.95)',
                            titleColor: '#2d3748',
                            bodyColor: '#4a5568',
                            bodyFont: { weight: 'bold', size: 14 },
                            borderColor: '#e2e8f0',
                            borderWidth: 1,
                            cornerRadius: 12,
                            padding: 12,
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
                            grid: { display: false },
                            ticks: {
                                font: { size: 11, weight: '600' },
                                color: '#4a5568',
                                cursor: 'pointer',
                            }
                        },
                        y: {
                            display: true,
                            grid: { color: 'rgba(0,0,0,0.06)' },
                            ticks: {
                                font: { size: 10, weight: '500' },
                                color: '#718096',
                                callback: function(value) {
                                    return formatCurrency(value);
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index',
                    },
                }
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
