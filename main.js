document.addEventListener('DOMContentLoaded', function() {
    const size = 40;
    let probs = createProbs(6, 6, size);
    let matrix = createTransMatrix(probs, size);
    //console.log(math.pow(matrix, 1000));
    let init = math.zeros(size, 1);
    init.set([0, 0], 1);
    //console.log(math.dot(matrix, init));
    //let fieldProbs = 
    let fieldProbs = math.ones(40).valueOf();
    createPlot(fieldProbs);
})

/**
 * @param {number} numDice1
 * @param {number} numDice2
 * @param {number} numfields
 * @returns {Array<number>}
 */
function createProbs(numDice1, numDice2, numFields) {
    let probs = new Array(numFields).fill(0);
    for (let i=1; i<numDice1+1; i++) {
        for (let j=1; j<numDice2+1; j++) {
            probs[i+j] += 1/numDice1 * 1/numDice2;
        }
    }

    return probs;
}

/** 
 * @param {Array<number>} probs
 * @param {number} size
 * @returns {math.Matrix} 
 */
function createTransMatrix(probs, size) {
    let matrix = math.zeros(size, size);
    for (let i=0; i<size; i++) {
        for (let j=0; j<probs.length; j++) {
            const idx = (i+j) % size;
            matrix.set([i, idx], probs[j]);
        }
    }

    return matrix;
}

function createPlot(probs) {
    let options = { series: [] };

    options.series.push({ data: new Array(11) });
    for (let i=0; i<11; i++) {
        options.series[0].data[10-i] = probs[i];
    }

    for (let i=0; i<9; i++) {
        let row = new Array(11).fill(null);
        row[0] = probs[11+i];
        row[10] = probs[18-i];
        options.series.push({
            data: row,
        });
    }

    options.series.push({ data: new Array(11) });
    for (let i=0; i<11; i++) {
        options.series[options.series.length-1].data[i] = probs[10+i];
    }

    options.dataLabels = { enabled: true };
    options.colors = ["#008FFB"];
    options.chart = { id: 'board', type: 'heatmap', height: 400, width: 400 };
    options.tooltip = {
        enabled: false,
    };
    options.xaxis = { 
        labels: { show: false },
        crosshairs: { show: false },
        tooltip: { enabled: false },
    };
    options.yaxis = { 
        labels: { show: false },
        crosshairs: { show: false },
        tooltip: { enabled: false },
    };
    console.log(options)
    let chart = new ApexCharts(document.querySelector("#board"), options);
    chart.render();

}
