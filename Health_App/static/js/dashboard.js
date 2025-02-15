document.addEventListener("DOMContentLoaded", function() {
  // Fetch data for the line chart (Rendez-vous over 6 months)
  fetch('/generate-plots/')
  .then(response => response.json())
  .then(data => {
    const ctxLine = document.getElementById('lineChart').getContext('2d');
    const lineChart = new Chart(ctxLine, {
      type: 'line',
      data: {
        labels: data.months,
        datasets: [{
          label: 'Rendez-vous',
          data: data.rendezvous_counts,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          fill: false
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });

// La réparition de revenus dans ler derniere 6 mois
fetch('/generate-plots/')
  .then(response => response.json())
  .then(data => {
    const ctxBar = document.getElementById('barChart').getContext('2d');
    const barChart = new Chart(ctxBar, {
      type: 'bar',
      data: {
        labels: data.months,
        datasets: [{
          label: 'Montant (MAD)',
          data: data.montant_totals,
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });

// Fetch data for the pie chart (Rendez-vous Status Distribution)
fetch('/rdv-status-distribution/')
  .then(response => response.json())
  .then(data => {
    const ctxPie = document.getElementById('pieChart').getContext('2d');
    const pieChart = new Chart(ctxPie, {
      type: 'pie',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
          ],
          borderWidth: 1
        }]
      }
    });
  });
  // la reparition des patients diabetique
fetch('/statistiques-diabete/')
.then(response => response.json())
.then(data => {
  const ctxDiabetes = document.getElementById('diabetesPieChart').getContext('2d');
  new Chart(ctxDiabetes, {
    type: 'pie',
    data: {
      labels: data.labels,
      datasets: [{
        data: data.data,
        backgroundColor: ['#ff6384', '#36a2eb'],
        borderColor: ['#ff6384', '#36a2eb'],
        borderWidth: 1
      }]
    }
  });
});

// les trois top payants patients dans ler dernieres 6 mois 
fetch('/montant-by-patient/')
  .then(response => response.json())
  .then(data => {
    const ctxDoughnut = document.getElementById('doughnutChart').getContext('2d');
    const doughnutChart = new Chart(ctxDoughnut, {
      type: 'doughnut',
      data: {
        labels: data.labels,  // Noms des 3 patients
        datasets: [{
          data: data.total_montants,  // Montants totaux des 3 patients
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
          ],
          borderWidth: 1
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: 'Top 3 Patients par Montant Dépensé (6 derniers mois)'
          }
        }
      }
    });
  });
  fetch("/evolution_statistiques_diabete/")  
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('evolutionDiabeteChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,  // Mois
                datasets: [
                    {
                        label: "Diabète détecté",
                        data: data.positive_counts,
                        borderColor: "red",
                        backgroundColor: "rgba(255, 0, 0, 0.2)",
                        fill: true
                    },
                    {
                        label: "Pas de diabète",
                        data: data.negative_counts,
                        borderColor: "green",
                        backgroundColor: "rgba(0, 255, 0, 0.2)",
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
    /// la réparition de la classification des mlaadies
    fetch("/statistiques-maladies/")  
          .then(response => response.json())
          .then(data => {
             
              const ctxPie = document.getElementById('maladiesPieChart').getContext('2d');
              new Chart(ctxPie, {
                  type: 'pie',
                  data: {
                      labels: data.labels_pie,
                      datasets: [{
                          data: data.data_pie,
                          backgroundColor: ['#93ff7a', '#29285f', '#ffcd56', '#4bc0c0'],
                          borderColor: ['#1e1e1e', '#8dd968', '#b18393', '#4bc0c0'],
                          borderWidth: 1
                      }]
                  }
              });
            


      //// l'évoluttion de la classification des maladies dans lers derniers 6 mous 
      const ctxLine = document.getElementById('maladiesLineChart').getContext('2d');
              new Chart(ctxLine, {
                  type: 'line',
                  data: {
                      labels: data.labels_line,
                      datasets: Object.keys(data.evolution_data).map(maladie => ({
                          label: maladie,
                          data: data.evolution_data[maladie],
                          borderColor: "#" + Math.floor(Math.random()*16777215).toString(16),
                          backgroundColor: "rgba(10, 231, 21, 0.2)",
                          fill: true
                      }))
                  },
                  options: {
                      responsive: true,
                      scales: {
                          y: {
                              beginAtZero: true
                          }
                      }
                  }
              });
            });
         
});
