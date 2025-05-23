import os
import re
import csv
import json

# Parses wrk output files into a CSV

RESULTS_DIR = "results"
OUTPUT_CSV = RESULTS_DIR + "/" + "results_summary.csv"

# Regex to extract key metrics from wrk output
regex = {
    "requests_per_sec": re.compile(r"Requests/sec:\s+([\d.]+)"),
    "latency_avg": re.compile(r"Latency\s+([\d.]+)(ms|s|us)"),
    "transfer_per_sec": re.compile(r"Transfer/sec:\s+([\d.]+)(\wB)"),
    "non_2xx": re.compile(r"Non-2xx or 3xx responses: (\d+)")
}

def normalize_latency(val, unit):
    if unit == "s":
        return float(val) * 1000
    if unit == "ms":
        return float(val)
    if unit == "us":
        return float(val) / 1000
    return float(val)

def normalize_transfer(val, unit):
    val = float(val)
    if unit == "kB":
        return val
    if unit == "MB":
        return val * 1024
    if unit == "GB":
        return val * 1024 * 1024
    return val

rows = []
for filename in os.listdir(RESULTS_DIR):
    if not filename.endswith(".txt"): continue
    framework = filename.replace(".txt", "")
    with open(os.path.join(RESULTS_DIR, filename)) as f:
        content = f.read()

        rps_match = regex["requests_per_sec"].search(content)
        latency_match = regex["latency_avg"].search(content)
        transfer_match = regex["transfer_per_sec"].search(content)
        non2xx_match = regex["non_2xx"].search(content)

        rps = float(rps_match.group(1)) if rps_match else 0
        latency = normalize_latency(latency_match.group(1), latency_match.group(2)) if latency_match else 0
        transfer = normalize_transfer(transfer_match.group(1), transfer_match.group(2)) if transfer_match else 0
        errors = int(non2xx_match.group(1)) if non2xx_match else 0

        rows.append({
            "framework": framework,
            "requests_per_sec": rps,
            "avg_latency_ms": latency,
            "transfer_kb_sec": transfer,
            "non_2xx": errors
        })

# Write to CSV
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Results written to {OUTPUT_CSV}")


# Embed the data directly into an HTML template
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Benchmark Results</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f8f9fa;
      color: #333;
      margin: 2rem;
    }
    h1 {
      text-align: center;
      margin-bottom: 2rem;
    }
    canvas {
      display: block;
      width: 100%;
      max-width: 1200px;
      max-height: 500px;
      height: 300px;
      margin: 3rem auto;
    }
    h2 {
      text-align: center;
      margin-top: 3rem;
      color: #444;
    }
    table {
      margin: 3rem auto;
      border-collapse: collapse;
      width: 100%;
      max-width: 1000px;
      font-size: 1rem;
      background: white;
      box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    th, td {
      padding: 12px 16px;
      border: 1px solid #ddd;
      text-align: center;
    }
    th {
      background-color: #f0f0f0;
      font-weight: bold;
    }
    tr:nth-child(even) {
      background-color: #f9f9f9;
    }
  </style>
</head>
<body>

<h1>🚀 Benchmark Results Dashboard</h1>

<h2>📈 Requests per Second</h2>
<canvas id="requestsChart"></canvas>

<h2>⏱️ Average Latency (ms)</h2>
<canvas id="latencyChart"></canvas>

<h2>📤 Transfer per Second (kB)</h2>
<canvas id="transferChart"></canvas>

<h2>📊 Full Results Table (Sorted by Requests/sec)</h2>
<table id="resultsTable">
  <thead>
    <tr>
      <th>Framework</th>
      <th>Requests/sec</th>
      <th>Avg Latency (ms)</th>
      <th>Transfer/sec (kB)</th>
    </tr>
  </thead>
  <tbody></tbody>
</table>

<script>
  const resultsData = __DATA__;

  function createChart(ctxId, label, data, color) {
    const ctx = document.getElementById(ctxId).getContext('2d');
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(d => d.framework),
        datasets: [{
          label,
          data: data.map(d => d.value),
          backgroundColor: color,
          borderColor: '#111',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  // Sort individually for each chart
  const rpsSorted = [...resultsData].sort((a, b) => a.requests_per_sec - b.requests_per_sec);
  const latencySorted = [...resultsData].sort((a, b) => b.avg_latency_ms - a.avg_latency_ms);
  const transferSorted = [...resultsData].sort((a, b) => a.transfer_kb_sec - b.transfer_kb_sec);

  createChart('requestsChart', 'Requests/sec', rpsSorted.map(d => ({ framework: d.framework, value: d.requests_per_sec })), '#0d6efd');
  createChart('latencyChart', 'Average Latency (ms)', latencySorted.map(d => ({ framework: d.framework, value: d.avg_latency_ms })), '#dc3545');
  createChart('transferChart', 'Transfer/sec (kB)', transferSorted.map(d => ({ framework: d.framework, value: d.transfer_kb_sec })), '#198754');

  // Tabel view
  const sortedData = [...resultsData].sort((a, b) => b.requests_per_sec - a.requests_per_sec);
  const tableBody = document.querySelector("#resultsTable tbody");

  sortedData.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.framework}</td>
      <td>${row.requests_per_sec.toFixed(2)}</td>
      <td>${row.avg_latency_ms.toFixed(2)}</td>
      <td>${row.transfer_kb_sec.toFixed(2)}</td>
    `;
    tableBody.appendChild(tr);
  });

</script>
</body>
</html>
"""

# Inject JSON directly
html_with_data = TEMPLATE_HTML.replace("__DATA__", json.dumps(rows, indent=2))

# Write to standalone HTML
with open("results_dashboard.html", "w") as f:
    f.write(html_with_data)

print("✅ Self-contained HTML dashboard written to results_dashboard.html")