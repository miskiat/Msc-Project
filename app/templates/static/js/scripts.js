document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('lineChart').getContext('2d');
    var chartData = JSON.parse(document.getElementById('lineChartData').textContent);

    new Chart(ctx, {
        type: 'line',
        data: chartData
    });
});
