const SIZE = 40;
/** @type {matn.Matrix} */
var gMatrix;
/** @type {Array<number>} */
var gProbs;
/** @type {ApexCharts} */
var gChart;

document.addEventListener('DOMContentLoaded', function() {
    gMatrix = math.zeros(SIZE, SIZE);
    gProbs = new Array(SIZE).fill(0);

    document.querySelector('#calc').addEventListener('click', function(e) {
        e.preventDefault();
        const steps = document.querySelector('#steps').value;
        console.log(steps)

        createFieldProbs(steps)
        updatePlot();
    })

    createTransMatrix();
    createFieldProbs(1);
    createPlot();
})

/**
 * @param {number} numDice1
 * @param {number} numDice2
 * @returns {Array<number>}
 */
function createDiceProbs(numDice1, numDice2) {
    let probs = new Array(SIZE).fill(0);
    for (let i=1; i<numDice1+1; i++) {
        for (let j=1; j<numDice2+1; j++) {
            probs[i+j] += 1/numDice1 * 1/numDice2;
        }
    }

    return probs;
}

function createTransMatrix() {
    let diceProbs = createDiceProbs(6, 6);
    for (let i=0; i<SIZE; i++) {
        for (let j=0; j<diceProbs.length; j++) {
            const idx = (i+j) % SIZE;
            gMatrix.set([i, idx], diceProbs[j]);
        }
    }
}

/**
 * @param {number} steps
 */
function createFieldProbs(steps) {
    let init = math.zeros(SIZE, 1);
    init.set([0, 0], 1);
    const probs = math.multiply(math.transpose(math.pow(gMatrix, steps)), init);
    gProbs = math.flatten(probs).valueOf();
}

/**
 * @return {Array<{data: Array<number|null>}>}
 */
function createSeriesFromProbs() {
    let series = [];
    series.push({ data: new Array(11) });
    for (let i=0; i<11; i++) {
        series[0].data[10-i] = gProbs[i];
    }

    for (let i=0; i<9; i++) {
        let row = new Array(11).fill(null);
        row[0] = gProbs[11+i];
        row[10] = gProbs[39-i];
        series.push({
            data: row,
        });
    }

    series.push({ data: new Array(11) });
    for (let i=0; i<11; i++) {
        series[series.length-1].data[i] = gProbs[20+i];
    }

    return series;
}

function createPlot() {
    let options = {
        series: createSeriesFromProbs(),
        dataLabels: { enabled: true },
        colors: ["#008FFB"],
        chart: { id: 'board', type: 'heatmap', height: 400, width: 400 },
        tooltip: {
            enabled: false,
        },
        xaxis: { 
            labels: { show: false },
            crosshairs: { show: false },
            tooltip: { enabled: false },
        },
        yaxis: { 
            labels: { show: false },
            crosshairs: { show: false },
            tooltip: { enabled: false },
        },
    };
    gChart = new ApexCharts(document.querySelector("#board"), options);
    gChart.render();
}

function updatePlot() {
    const newSeries = createSeriesFromProbs();
    gChart.updateSeries(newSeries);
}
