
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

fetch('data/pretty_plt_count_by_year.json')
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
          x: {
            stacked: true,
            title: {
              display: true,
              text: 'Year', // Custom x-axis label
              font: {
                size: 14, // Font size for x-axis label
                weight: 'bold'
              },
              padding: { top: 10 }
            }
          },
          y: {
            beginAtZero: true,
            stacked: true,
            title: {
              display: true,
              text: 'Number of articles', // Custom y-axis label
              font: {
                size: 14, // Font size for y-axis label
                weight: 'bold'
              },
              padding: { bottom: 10 }
            }
          }
        },
        plugins: {
          legend: { display: true }
        }
      }
    });
  })
  .catch(error => console.error('Error loading JSON:', error));

fetch('data/pretty_plt_name_year_counts.json')
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
          x: {
            stacked: true,
            title: {
              display: true,
              text: 'Year', 
              font: {
                size: 14, 
                weight: 'bold'
              },
              padding: { top: 10 }
            }
          },
          y: {
            beginAtZero: true,
            stacked: true,
            title: {
              display: true,
              text: 'Number of articles',
              font: {
                size: 14,
                weight: 'bold'
              },
              padding: { bottom: 10 }
            }
          }
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


  // Change chart
  // Fetch the JSON data
fetch('data/pretty_change.json')
.then(response => response.json())
  .then(data => {
    // Sort datasets by relative_change in descending order
    const allDatasets = data.datasets.sort((a, b) => b.relative_change - a.relative_change);
    const checkboxContainer = document.getElementById('multiLabelDropdown');
    const searchInput = document.getElementById('searchInput');

    // Track which items are checked
    const checkedStates = new Set();

    // Function to render checkboxes based on a filtered list
    function renderCheckboxes(filteredDatasets) {
      checkboxContainer.innerHTML = ''; // Clear existing checkboxes

      filteredDatasets.forEach((dataset, index) => {
        const checkboxLabel = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = dataset.label; // Store label as unique identifier
        checkbox.checked = checkedStates.has(dataset.label); // Set checked state based on memory
        checkboxLabel.appendChild(checkbox);
        checkboxLabel.appendChild(document.createTextNode(dataset.label));
        checkboxContainer.appendChild(checkboxLabel);
        checkboxContainer.appendChild(document.createElement('br'));

        // Attach event listener to track checked items
        checkbox.addEventListener('change', function () {
          if (checkbox.checked) {
            checkedStates.add(dataset.label);
          } else {
            checkedStates.delete(dataset.label);
          }
          updateChart(); // Update chart when a checkbox is toggled
        });
      });
    }

    // Initial render with all datasets
    renderCheckboxes(allDatasets);

    // Event listener to filter checkboxes as user types in the search box
    searchInput.addEventListener('input', () => {
      const searchText = searchInput.value.toLowerCase();
      const filteredDatasets = allDatasets.filter(dataset =>
        dataset.label.toLowerCase().includes(searchText)
      );
      renderCheckboxes(filteredDatasets); // Render only for filtered items
    });

    // Set up the initial chart (empty)
    const ctx = document.getElementById('relativeChangeChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [{
          label: 'Relative Change',
          data: [],
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
          x: { beginAtZero: true },
          y: { beginAtZero: true }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });

    // Function to update chart based on checked boxes
    function updateChart() {
      // Only use datasets corresponding to checked labels
      const selectedDatasets = allDatasets.filter(dataset => checkedStates.has(dataset.label));

      // Update chart labels and data
      chart.data.labels = selectedDatasets.map(dataset => dataset.label);
      chart.data.datasets[0].data = selectedDatasets.map(dataset => dataset.relative_change);

      chart.update(); // Refresh the chart with new data
    }
  })
  .catch(error => console.error('Error loading JSON:', error));