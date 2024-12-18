// Helper function to format percentages
function formatPercentage(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return '0,0';
  }
  const multiplied = value * 100;
  const rounded = multiplied.toFixed(1);
  const withComma = rounded.replace('.', ',');
  return withComma;
}

// Fetch the data and initialize the app
let electionData = [];
let electionData2019 = [];

// Function to fetch and parse CSV data
function fetchData(url, dataArray) {
  return fetch(url)
    .then(response => response.text())
    .then(csvText => {
      const parsedData = Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
      });
      dataArray.push(...parsedData.data);
    })
    .catch(error => {
      console.error(`Error fetching data from ${url}:`, error);
      alert(`Ocurrió un error al obtener los datos de ${url}.`);
    });
}

// Fetch both datasets in parallel
Promise.all([
  fetchData('elecciones_24.csv', electionData),
  fetchData('elecciones_19.csv', electionData2019)
]).then(() => {
  console.log('Both datasets have been loaded.');
});

// Vertical line plugin to add to both graphs
const verticalLinePlugin = {
  id: 'verticalLinePlugin',
  afterDraw: (chart) => {
    const ctx = chart.ctx;
    const xAxis = chart.scales['x'];
    const yAxis = chart.scales['y'];

    // Calculate the position of the spacer label
    const spacerIndex = 2; // Index of the spacer label

    // Get the pixel for the spacer label
    const xPos = xAxis.getPixelForTick(spacerIndex);

    // Draw the vertical line
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(xPos, yAxis.top);
    ctx.lineTo(xPos, yAxis.bottom);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#000'; // Black color
    ctx.stroke();
    ctx.restore();
  }
};

// Event listener for the Consultar button
document.getElementById('consultar').addEventListener('click', function () {
  const serieInput = document.getElementById('serie').value.trim().toUpperCase();
  const numberInput = parseInt(document.getElementById('number').value);

  const outputDiv = document.getElementById('output');
  outputDiv.innerHTML = '';

  if (!serieInput || serieInput.length !== 3 || isNaN(numberInput)) {
    outputDiv.innerHTML = 'Por favor, ingrese una serie de 3 letras y un número válido.';
    return;
  }

  // Ensure data is loaded before proceeding
  if (electionData.length === 0) {
    outputDiv.innerHTML = 'Los datos de 2024 aún no se han cargado. Por favor, inténtelo de nuevo en unos segundos.';
    return;
  }

  // Find the matching data in both datasets
  const matchingData = electionData.find(item => {
    return item.serie === serieInput && numberInput >= item.desde && numberInput <= item.hasta;
  });

  let matchingData2019 = null;
  if (electionData2019.length > 0) {
    matchingData2019 = electionData2019.find(item => {
      return item.serie === serieInput && numberInput >= item.desde && numberInput <= item.hasta;
    });
  }

  if (!matchingData) {
    outputDiv.innerHTML = 'No se encontraron resultados para los datos proporcionados en 2024.';
    return;
  }

  // Display the first message and chart
  const messageBeforeChart = `
    <p>En el circuito donde votaste, Yamandú Orsi pasó de obtener <strong>${formatPercentage(matchingData.fa)}%</strong> de los votos en octubre al <strong>${formatPercentage(matchingData.orsi)}%</strong> en noviembre, mientras que los partidos de la Coalición Republicana (Álvaro Delgado) pasaron de obtener <strong>${formatPercentage(matchingData.core)}%</strong> de los votos en octubre al <strong>${formatPercentage(matchingData.delgado)}%</strong> en noviembre.</p>
  `;
  outputDiv.innerHTML = messageBeforeChart;

  const labels = [
    'Orsi (Nov)', 'Delgado (Nov)', '', 'FA (Oct)', 'PN', 'PC', 'CA', 'PI', 'PCA', 'IS', 'PERI', 'PCN', 'AP'
  ];
  const dataValues = [
    parseFloat(matchingData.orsi) * 100 || 0,
    parseFloat(matchingData.delgado) * 100 || 0,
    null,
    parseFloat(matchingData.fa) * 100 || 0,
    parseFloat(matchingData.pn) * 100 || 0,
    parseFloat(matchingData.pc) * 100 || 0,
    parseFloat(matchingData.ca) * 100 || 0,
    parseFloat(matchingData.pi) * 100 || 0,
    parseFloat(matchingData.pca) * 100 || 0,
    parseFloat(matchingData.is) * 100 || 0,
    parseFloat(matchingData.peri) * 100 || 0,
    parseFloat(matchingData.pcn) * 100 || 0,
    parseFloat(matchingData.ap) * 100 || 0
  ];

  createChart('myChart', outputDiv, labels, dataValues, 'Resultados en el Circuito en 2024: Noviembre vs Octubre');

  if (matchingData2019) {
    const messageAfterChart = `
      <h3>¿Qué pasó en 2019?</h3>
      <p>En el circuito donde votaste en 2019, el Frente Amplio (Daniel Martínez) pasó de obtener <strong>${formatPercentage(matchingData2019.fa)}%</strong> de los votos en octubre al <strong>${formatPercentage(matchingData2019.martinez)}%</strong> en noviembre.</p>
    `;
    outputDiv.insertAdjacentHTML('beforeend', messageAfterChart);

    const labels2019 = [
      'Martínez (Nov)', 'Lacalle (Nov)', '', 'FA (Oct)', 'PN', 'PC', 'CA', 'PI', 'PG', 'PERI', 'AP', 'PT', 'PD'
    ];
    const dataValues2019 = [
      parseFloat(matchingData2019.martinez) * 100 || 0,
      parseFloat(matchingData2019.lacalle) * 100 || 0,
      null,
      parseFloat(matchingData2019.fa) * 100 || 0,
      parseFloat(matchingData2019.pn) * 100 || 0,
      parseFloat(matchingData2019.pc) * 100 || 0,
      parseFloat(matchingData2019.ca) * 100 || 0,
      parseFloat(matchingData2019.pi) * 100 || 0,
      parseFloat(matchingData2019.pg) * 100 || 0,
      parseFloat(matchingData2019.peri) * 100 || 0,
      parseFloat(matchingData2019.ap) * 100 || 0,
      parseFloat(matchingData2019.pt) * 100 || 0,
      parseFloat(matchingData2019.pd) * 100 || 0
    ];

    createChart('myChart2019', outputDiv, labels2019, dataValues2019, 'Resultados en el Circuito en 2019: Noviembre vs Octubre');
  }
});

// Function to create a chart
function createChart(chartId, container, labels, dataValues, titleText) {
  const canvasElement = document.createElement('canvas');
  canvasElement.id = chartId;
  canvasElement.style.maxWidth = '100%';
  container.appendChild(canvasElement);

  const ctx = canvasElement.getContext('2d');

  if (window[chartId] && typeof window[chartId].destroy === 'function') {
    window[chartId].destroy();
  }

  window[chartId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Porcentaje de Votos',
        data: dataValues,
        backgroundColor: [
          '#006400', '#0000FF', 'rgba(0,0,0,0)', '#006400', '#87CEEB', '#FF0000', '#FFA500',
          '#800080', '#FFFF00', '#008000', '#90EE90', '#000000', '#FF6347'
        ]
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: titleText
        },
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const value = context.raw || 0;
              return `${value.toFixed(1)}%`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    },
    plugins: [verticalLinePlugin] // Apply the vertical line plugin
  });
}
