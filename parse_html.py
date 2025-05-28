import sys
import os
import re
import csv
import json
import platform
import psutil
import subprocess
from datetime import datetime, timezone

# Parses wrk output files into a CSV

RESULTS_DIR = "results/raw"
OUTPUT_CSV = "results/results_summary.csv"
OUTPUT_HTML = "results/results_dashboard.html"

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

def get_os_name():
    try:
        import distro
    except ImportError:
        distro = None  # We'll handle missing distro gracefully

    if platform.system() == "Darwin":
        mac_ver = platform.mac_ver()[0]  # e.g., '13.4.1'
        os_info = f"macOS {mac_ver}"
    elif platform.system() == "Linux":
        if distro:
            name = distro.name(pretty=True)  # 'Ubuntu 24.04 LTS'
            if not name:
                # fallback if pretty name missing
                name = f"{distro.id()} {distro.version()}"
            os_info = name
        else:
            # If distro not installed, fallback to platform info
            os_info = f"Linux {platform.release()}"
    else:
        os_info = f"{platform.system()} {platform.release()}"
    
    return os_info

def get_cpu_name():
    system = platform.system()
    cpu_name = "Unknown CPU"

    if system == "Darwin":
        try:
            cpu_name = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                text=True
            ).strip()
        except Exception:
            pass

    elif system == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu_name = line.split(":", 1)[1].strip()
                        break
        except Exception:
            pass

    return cpu_name

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
    #envTable {
      margin: 3rem auto;
      border-collapse: collapse;
      width: 100%;
      max-width: 800px;
      font-size: 1rem;
      background: white;
      box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    #envTable th, #envTable td {
      padding: 10px 14px;
      border: 1px solid #ccc;
      text-align: left;
    }
    #envTable th {
      background-color: #f0f0f0;
      width: 200px;
    }
    footer {
      text-align: center; 
      margin-top: 80px; 
      font-size: 0.9em; 
      color: #888;
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

<h2>🛠 Benchmark Environment</h2>
<table id="envTable">
  <tbody>
    <tr><th>OS</th><td id="os">__OS__</td></tr>
    <tr><th>CPU</th><td id="cpu">__CPU__</td></tr>
    <tr><th>RAM</th><td id="ram">__RAM__</td></tr>
    <tr><th>Date</th><td id="date">__DATE__</td></tr>
    <tr><th>Benchmark Command</th><td><code>wrk -t__CORES__ -c1000 -d60s -s post.lua</code></td></tr>
    <tr><th>Python Version</th><td id="date">__PYVER__</td></tr>
    <tr><th>Node Version</th><td id="date">__NODEVER__</td></tr>
    <tr><th>Bun Version</th><td id="date">__BUNVER__</td></tr>
    <tr><th>Deno Version</th><td id="date">__DENOVER__</td></tr>
    <tr><th>Go Version</th><td id="date">__GOVER__</td></tr>
  </tbody>
</table>

<footer>
  Results generated using <a href="https://github.com/Drarox/Backend-Benchmark" target="_blank" style="color: #555; text-decoration: none;">
    Drarox/Backend-Benchmark
  </a>
</footer>

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

# Inject environment
date_info = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

# Sytem infos
os_info = get_os_name()

cpu_name = get_cpu_name()
cpu_cores = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True) or "Unknown"
cpu_info = f"{cpu_name} ({cpu_cores} cores)"

ram_info = f"{round(psutil.virtual_memory().total / (1024**3))} GB"

# Python version
pyver = sys.version.split()[0]  # e.g. '3.11.4'

# Node.js version
try:
    nodever = subprocess.check_output(["node", "--version"], text=True).strip()
except Exception:
    nodever = "Node not found"

# Bun version
try:
    bunver = subprocess.check_output(["bun", "--version"], text=True).strip()
except Exception:
    bunver = "Bun not found"

# Deno version
try:
    deno_full = subprocess.check_output(["deno", "--version"], text=True).strip().split("\n")[0]
    # deno_full example: "deno 1.35.2 (release, x86_64-unknown-linux-gnu)"
    denover = " ".join(deno_full.split()[:2])  # keeps "deno 1.35.2"
except Exception:
    denover = "Deno not found"

# Go version
try:
    gover = subprocess.check_output(["go", "version"], text=True).strip()
    # go version output example: 'go version go1.21.0 linux/amd64'
    # Extract just 'go1.21.0'
    gover = gover.split()[2]
except Exception:
    gover = "Go not found"

html_with_data = html_with_data \
    .replace("__OS__", os_info) \
    .replace("__CPU__", cpu_info) \
    .replace("__CORES__", str(cpu_cores)) \
    .replace("__RAM__", ram_info) \
    .replace("__DATE__", date_info) \
    .replace("__PYVER__", pyver) \
    .replace("__NODEVER__", nodever) \
    .replace("__BUNVER__", bunver) \
    .replace("__DENOVER__", denover) \
    .replace("__GOVER__", gover)

# Write to standalone HTML
with open(OUTPUT_HTML, "w") as f:
    f.write(html_with_data)

print(f"✅ Self-contained HTML dashboard written to {OUTPUT_HTML}")