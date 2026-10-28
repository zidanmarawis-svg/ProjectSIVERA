// static/js/dashboard.js
// Mengambil data dari endpoint API dan render chart.
fetch('/api/dashboard')
  .then(r => r.json())
  .then(data => {
    const ctx = document.getElementById('chartStatus');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Jumlah Pengajuan',
          data: data.values,
          backgroundColor: ['#0d6efd', '#198754', '#dc3545', '#ffc107']
        }]
      }
    });
  });