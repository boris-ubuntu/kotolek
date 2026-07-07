class GraphComponent {
    constructor() {
        this.canvas = document.getElementById('balance-graph');
        this.chart = null;
    }
    async update() {
        try {
            const data = await API.getDailyBalance();
            if (data && data.length > 0) {
                this.render(data);
            } else {
                this.clearChart();
            }
        } catch (error) {
            console.error('Failed to load graph:', error);
            this.clearChart();
        }
    }
    render(data) {
        if (!data || data.length === 0) {
            this.clearChart();
            return;
        }
        const labels = data.map(function(item) {
            const date = new Date(item.date);
            return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' });
        });
        const values = data.map(function(item) { return item.balance; });
        
        const gradient = this.canvas.getContext('2d').createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, 'rgba(102, 126, 234, 0.4)');
        gradient.addColorStop(0.5, 'rgba(102, 126, 234, 0.15)');
        gradient.addColorStop(1, 'rgba(102, 126, 234, 0)');
        
        if (this.chart) {
            this.chart.data.labels = labels;
            this.chart.data.datasets[0].data = values;
            this.chart.update();
        } else {
            this.chart = new Chart(this.canvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        borderColor: '#667eea',
                        backgroundColor: gradient,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: '#667eea',
                        pointHoverBorderColor: '#fff',
                        pointHoverBorderWidth: 2,
                        borderWidth: 3,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(255,255,255,0.95)',
                            titleColor: '#2d3748',
                            bodyColor: '#667eea',
                            bodyFont: { weight: 'bold', size: 14 },
                            borderColor: '#e2e8f0',
                            borderWidth: 1,
                            cornerRadius: 12,
                            padding: 12,
                            callbacks: {
                                label: function(context) {
                                    return 'Баланс: ' + formatCurrency(context.parsed.y);
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: { display: false },
                            ticks: {
                                font: { size: 10, weight: '500' },
                                maxTicksLimit: 10,
                                color: '#a0aec0',
                            }
                        },
                        y: {
                            display: true,
                            grid: { color: 'rgba(0,0,0,0.04)' },
                            ticks: {
                                font: { size: 10, weight: '500' },
                                color: '#a0aec0',
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
