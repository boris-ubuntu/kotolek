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

    render(rawData) {
        if (!rawData || rawData.length === 0) {
            this.clearChart();
            return;
        }

        // Данные уже приходят за 31 день из API с кумулятивным балансом
        const labels = [];
        const values = [];
        let lastKnown = 0;

        rawData.forEach(function(item) {
            const dayNum = new Date(item.date + 'T00:00:00').getDate();
            labels.push(String(dayNum));
            if (item.balance !== null && item.balance !== undefined) {
                lastKnown = item.balance;
            }
            values.push(lastKnown);
        });

        // Цвет столбца: синий для положительного баланса, красный для отрицательного
        const BLUE = '#00aff5';
        const RED = '#f27362';
        const barColors = values.map(function(v) { return v >= 0 ? BLUE : RED; });

        if (this.chart) {
            this.chart.data.labels = labels;
            this.chart.data.datasets[0].data = values;
            this.chart.data.datasets[0].backgroundColor = barColors;
            this.chart.update();
        } else {
            this.chart = new Chart(this.canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            data: values,
                            backgroundColor: barColors,
                            borderRadius: 3,
                            borderSkipped: false,
                            categoryPercentage: 0.95,
                            barPercentage: 1.0,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    devicePixelRatio: window.devicePixelRatio || 2,
                    layout: {
                        padding: { top: 30, right: 4, bottom: 26, left: 4 }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: { display: false },
                            border: { display: false },
                            ticks: {
                                font: { size: 10, weight: '500' },
                                maxTicksLimit: 16,
                                autoSkip: true,
                                color: '#a0aec0',
                            }
                        },
                        // Шкала скрыта — вместо неё подписываем топ +/- значения
                        y: {
                            display: false,
                            grid: { display: false },
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index',
                    },
                },
                plugins: [{
                    id: 'topLabels',
                    afterDatasetsDraw(chart) {
                        const { ctx } = chart;
                        const meta = chart.getDatasetMeta(0);
                        if (!meta.data || meta.data.length === 0) return;

                        const data = chart.data.datasets[0].data;
                        let maxIdx = 0, minIdx = 0;
                        for (let i = 1; i < data.length; i++) {
                            if (data[i] > data[maxIdx]) maxIdx = i;
                            if (data[i] < data[minIdx]) minIdx = i;
                        }

                        function drawMarker(idx, prefix) {
                            const bar = meta.data[idx];
                            const value = data[idx];
                            const x = bar.x;
                            // Для положительного — верх столбца (bar.y), для отрицательного — низ (bar.y)
                            const y = bar.y;
                            const color = value >= 0 ? BLUE : RED;

                            const text = prefix + formatCurrency(value);
                            ctx.save();
                            ctx.font = 'bold 12px Segoe UI, Tahoma, sans-serif';
                            const tw = ctx.measureText(text).width;
                            let tx = x;
                            const minX = tw / 2 + 4;
                            const maxX = chart.width - tw / 2 - 4;
                            if (tx < minX) tx = minX;
                            if (tx > maxX) tx = maxX;

                            ctx.textAlign = 'center';
                            // Положительный: подпись ВЫШЕ верха столбца.
                            // Отрицательный: подпись НИЖЕ низа столбца (не наезжает).
                            ctx.textBaseline = value >= 0 ? 'bottom' : 'top';
                            const ty = value >= 0 ? y - 6 : y + 6;
                            ctx.fillStyle = color;
                            ctx.shadowColor = 'rgba(0,0,0,0.6)';
                            ctx.shadowBlur = 4;
                            ctx.fillText(text, tx, ty);
                            ctx.restore();
                        }

                        drawMarker(maxIdx, '▲ ');
                        if (minIdx !== maxIdx) drawMarker(minIdx, '▼ ');
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

const BLUE = '#00aff5';
const RED = '#f27362';