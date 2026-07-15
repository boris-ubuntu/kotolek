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
            return;
        }

        this.chart = new Chart(this.canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#32323e',
                    hoverOffset: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '62%',
                // Минимальные поля — пончи к заполняет всю карточку,
                // подписи рисуются внутри сегментов (не обрезаются).
                layout: {
                    padding: 6
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        bodyFont: { family: 'Segoe UI, Tahoma, sans-serif', size: 13 },
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = ((context.raw / total) * 100).toFixed(1);
                                return ' ' + context.label + ': ' + formatCurrency(context.raw) + ' (' + pct + '%)';
                            }
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (!elements || elements.length === 0) return;
                    const index = elements[0].index;
                    const groupName = this.chart.data.labels[index];
                    if (!groupName) return;

                    const now = new Date();
                    const year = now.getFullYear();
                    const month = now.getMonth() + 1;
                    window.location.href =
                        '/category-detail.html?year=' + year +
                        '&month=' + month +
                        '&group=' + encodeURIComponent(groupName);
                }
            },
            plugins: [{
                id: 'innerLabels',
                afterDraw(chart) {
                    const { ctx, data, chartArea } = chart;
                    const meta = chart.getDatasetMeta(0);
                    if (!meta.data || meta.data.length === 0) return;

                    const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                    const centerX = chartArea.left + chartArea.width / 2;
                    const centerY = chartArea.top + chartArea.height / 2;
                    const outerRadius = meta.data[0].outerRadius;
                    const innerRadius = meta.data[0].innerRadius;

                    const isNarrow = chart.width < 500;
                    const nameFont = isNarrow ? 11 : 13;
                    const pctFont = isNarrow ? 10 : 12;

                    ctx.save();
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';

                    for (let i = 0; i < data.labels.length; i++) {
                        const arc = meta.data[i];
                        const angle = arc.endAngle - arc.startAngle;
                        // Слишком маленькие сегменты не подписываем, чтобы не было каши
                        if (angle < 0.18) continue;

                        const midAngle = arc.startAngle + angle / 2;
                        const r = (innerRadius + outerRadius) / 2;
                        const x = centerX + Math.cos(midAngle) * r;
                        const y = centerY + Math.sin(midAngle) * r;
                        const value = data.datasets[0].data[i];
                        const pct = ((value / total) * 100).toFixed(1);

                        ctx.fillStyle = '#ffffff';
                        ctx.shadowColor = 'rgba(0,0,0,0.65)';
                        ctx.shadowBlur = 3;

                        ctx.font = 'bold ' + nameFont + 'px Segoe UI, Tahoma, sans-serif';
                        ctx.fillText(data.labels[i], x, y - (isNarrow ? 7 : 8));

                        ctx.font = pctFont + 'px Segoe UI, Tahoma, sans-serif';
                        ctx.fillStyle = 'rgba(255,255,255,0.85)';
                        ctx.fillText(pct + '%', x, y + (isNarrow ? 6 : 7));
                    }

                    ctx.restore();
                }
            }, {
                id: 'centerText',
                beforeDraw: function(chart) {
                    const width = chart.width;
                    const height = chart.height;
                    const ctx = chart.ctx;
                    ctx.restore();
                    const fontSize = (height / 150).toFixed(2);
                    ctx.font = 'bold ' + fontSize + 'em Segoe UI, Tahoma, sans-serif';
                    ctx.textBaseline = 'middle';
                    const text = formatCurrency(totalExpenses);
                    const textY = height / 2;
                    ctx.fillStyle = '#e2e8f0';
                    ctx.textAlign = 'center';
                    ctx.fillText(text, width / 2, textY);
                    ctx.save();
                }
            }]
        });
    }

    clearChart() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}