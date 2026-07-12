class ChartComponent {
    constructor() {
        this.canvas = document.getElementById('expense-chart');
        this.totalElement = document.getElementById('month-total');
        this.chart = null;
    }
    async update() {
        try {
            const data = await API.getExpensesByCategory();
            const balance = await API.getBalance();
            this.render(data, balance);
        } catch (error) {
            console.error('Failed to load chart:', error);
            this.clearChart();
        }
    }
    render(data, balance) {
        const totalExpenses = balance ? balance.month_expenses : 0;
        if (!data || data.length === 0 || totalExpenses === 0) {
            this.clearChart();
            return;
        }
        
        const groups = {};
        for (let i = 0; i < data.length; i++) {
            const item = data[i];
            const groupName = getCategoryGroup(item.name);
            const groupColor = getCategoryColorByGroup(groupName);
            if (!groups[groupName]) {
                groups[groupName] = {
                    name: groupName,
                    color: groupColor,
                    total: 0
                };
            }
            groups[groupName].total += item.total;
        }
        
        const labels = Object.keys(groups).map(function(key) {
            return groups[key].name;
        });
        const values = Object.keys(groups).map(function(key) {
            return groups[key].total;
        });
        const colors = Object.keys(groups).map(function(key) {
            return groups[key].color;
        });
        
        if (this.chart) {
            this.chart.data.labels = labels;
            this.chart.data.datasets[0].data = values;
            this.chart.data.datasets[0].backgroundColor = colors;
            this.chart.update();
        } else {
            this.chart = new Chart(this.canvas, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: colors,
                        borderWidth: 3,
                        borderColor: '#fff',
                        hoverOffset: 10,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    cutout: '60%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 8,
                                font: {
                                    size: 11,
                                    weight: '500',
                                },
                                usePointStyle: true,
                                pointStyle: 'rectRounded',
                                pointStyleWidth: 20,
                                generateLabels: function(chart) {
                                    const data = chart.data;
                                    return data.labels.map(function(label, i) {
                                        return {
                                            text: label + '  ' + formatCurrency(data.datasets[0].data[i]),
                                            fillStyle: data.datasets[0].backgroundColor[i],
                                            strokeStyle: data.datasets[0].backgroundColor[i],
                                            pointStyle: 'rectRounded',
                                            index: i,
                                        };
                                    });
                                }
                            }
                        }
                    }
                },
                plugins: [{
                    id: 'centerText',
                    beforeDraw: function(chart) {
                        const width = chart.width;
                        const height = chart.height;
                        const ctx = chart.ctx;
                        ctx.restore();
                        const fontSize = (height / 160).toFixed(2);
                        ctx.font = 'bold ' + fontSize + 'em sans-serif';
                        ctx.textBaseline = 'middle';
                        const text = formatCurrency(totalExpenses);
                        const textY = height / 2 - 25;
                        ctx.fillStyle = '#2d3748';
                        ctx.textAlign = 'center';
                        ctx.fillText(text, width/2, textY);
                        ctx.save();
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
