
// Make the top 10 most popular chart

// Define color palette 
const colorPalette = [
  'rgba(75, 192, 192, 0.6)',
  'rgba(255, 99, 132, 0.6)',
  'rgba(54, 162, 235, 0.6)',
  'rgba(255, 206, 86, 0.6)',
  'rgba(153, 102, 255, 0.6)',
  'rgba(255, 159, 64, 0.6)',
  'rgba(201, 203, 207, 0.6)',
  'rgba(0, 123, 255, 0.6)',
  'rgba(220, 53, 69, 0.6)',
  'rgba(40, 167, 69, 0.6)'
];

fetch('data/plt_count_by_year.json')
  .then(response => response.json())
  .then(data => {
    // Access labels and datasets directly from the data object
    const labels = data.labels;
    // Map each label to a color
    const datasets = data.datasets.map((dataset, index) => ({
      ...dataset,
      backgroundColor: colorPalette[index % colorPalette.length],
      borderColor: colorPalette[index % colorPalette.length].replace('0.6', '1'),
      borderWidth: 1
    }));

    // Log to verify the data structure (see console in "Inspect" mode)
    console.log("Labels (Years):", labels);
    console.log("Datasets:", datasets);

    // Get the 2D context of the canvas element by ID
    const ctx2 = document.getElementById('popular10Chart').getContext('2d');

    // Configure and render the Chart.js bar chart
    new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        scales: {
          x: { stacked: true },
          y: { beginAtZero: true, stacked: true }
        },
        plugins: {
          legend: { display: true }
        }
      }
    });
  })
  .catch(error => console.error('Error loading JSON:', error));

fetch('data/plt_name_year_counts.json')
  .then(response => response.json())
  .then(data => {
    const labels = data.labels;
    const datasets = data.datasets;

    // Populate dropdown with dataset labels
    const dropdown = document.getElementById('labelSelect');
    datasets.forEach((dataset, index) => {
      const option = document.createElement('option');
      option.value = index; // Store index to retrieve dataset later
      option.text = dataset.label;
      dropdown.appendChild(option);
    });

    // Create the initial empty chart
    const ctx = document.getElementById('lineChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: []
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        },
        plugins: {
          legend: { display: true }
        }
      }
    });

    // Event listener for dropdown selection
    dropdown.addEventListener('change', function () {
      const selectedIndex = dropdown.value;
      if (selectedIndex === "") {
        chart.data.datasets = []; // Clear chart if no selection
      } else {
        const selectedDataset = datasets[selectedIndex];
        chart.data.datasets = [{
          label: selectedDataset.label,
          data: selectedDataset.data,
          borderColor: selectedDataset.borderColor || 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderWidth: 2
        }];
      }
      chart.update(); // Refresh the chart to show the selected data
    });
  })
  .catch(error => console.error('Error loading JSON:', error));