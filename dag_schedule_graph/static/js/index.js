import Chart from 'chart.js';
import moment from 'moment';
import {DATE_TIME_FORMAT, getDatasets, getXLabel} from './chart-helper.js';

moment.tz.setDefault('UTC');

function createChart(canvas, fromTimestamp, toTimestamp, dagSchedules) {
    const ctx = canvas.getContext('2d');
    const datasets = getDatasets(dagSchedules);
    const xLabel = getXLabel(fromTimestamp, toTimestamp);

    new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: datasets
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                xAxes: [
                    {
                        display: true,
                        type: 'time',
                        time: {
                            unit: 'hour',
                            unitStepSize: 1,
                            displayFormats: {
                                hour: 'HH:mm'
                            },
                            tooltipFormat: DATE_TIME_FORMAT
                        },
                        ticks: {
                            min: fromTimestamp,
                            max: toTimestamp
                        },
                        scaleLabel: {
                            display: true,
                            labelString: xLabel
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'DAG Count'
                        }
                    }
                ]
            },
            tooltips: {
                callbacks: {
                    title: function (tooltipItems, _data) {
                        const tooltipItem = tooltipItems[0];
                        return tooltipItem.yLabel + ' DAGs at ' + tooltipItem.xLabel;
                    },
                    label: function (tooltipItem, data) {
                        return data.datasets[tooltipItem.datasetIndex].label || [];
                    }
                }
            }
        }
    });
}

window.addEventListener('DOMContentLoaded', (event) => {
    const {fromTimestamp, toTimestamp, dagSchedules} = DAGScheduleGraph;
    const canvas = document.getElementById('chart');
    createChart(canvas, fromTimestamp, toTimestamp, dagSchedules);
});
