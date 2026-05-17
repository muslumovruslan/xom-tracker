let globalData = {};

async function loadData() {

    const response = await fetch('data/latest.json');

    globalData = await response.json();

    drawChart('1D');
}

function drawChart(timeframe) {

    const data = globalData[timeframe];

    const trace = {
        x: data.map(d => d.Date),

        open: data.map(d => d.Open),
        high: data.map(d => d.High),
        low: data.map(d => d.Low),
        close: data.map(d => d.Close),

        type: 'candlestick',

        increasing: {
            line: { color: 'green' }
        },

        decreasing: {
            line: { color: 'red' }
        }
    };

    const layout = {

        title: `XOM Candlestick Chart (${timeframe})`,

        dragmode: 'zoom',

        xaxis: {
            rangeslider: {
                visible: false
            }
        },

        yaxis: {
            autorange: true
        },

        height: 700
    };

    Plotly.newPlot('chart', [trace], layout);
}

function saveCurrentData() {

    const blob = new Blob(
        [JSON.stringify(globalData, null, 2)],
        { type: 'application/json' }
    );

    const a = document.createElement('a');

    a.href = URL.createObjectURL(blob);

    const date = new Date().toISOString();

    a.download = `XOM_${date}.json`;

    a.click();
}

loadData();