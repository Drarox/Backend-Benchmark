# Backend Benchmark

This project automates benchmarks of different backend frameworks for handling a simple JSON-processing POST route and creates a detailed HTML report with charts summarizing the results.

## 📦 Frameworks Covered

- **Python**: Flask, FastAPI  
- **JavaScript Runtimes**:
  - **Node-based**: Node (native), Express, Fastify, NestJS (Express), NestJS (Fastify)  
  - **Bun**  
  - **Deno** (using `Deno.serve`, native HTTP server)
- **Go**: Gin, Echo, Fiber, Native `net/http`

## 🔬 Benchmark Scenario

### Route: `POST /process`
- Input JSON: `{ "numbers": [1, 2, 3, 4, 5] }`
- Task: Compute the sum of squares of the numbers
- Output JSON: `{ "result": 55 }`

## 🔧 Prerequisites

Install the following tools:

* [Python 3.11+](https://www.python.org/)
* [Node.js (LTS)](https://nodejs.org/)
* [Go](https://golang.org/)
* [Deno](https://deno.land/)
* [Bun](https://bun.sh/)
* [`wrk`](https://github.com/wg/wrk)

Ensure each tool is available in your `PATH`.


## 🚀 Usage

#### 1. Clone & enter project

```bash
git clone https://github.com/Drarox/Backend-Benchmark.git
cd backend-benchmark
```

#### 2. Run presetup (install dependencies per framework)

```bash
./benchmark_presetup.sh
```

#### 3. Run benchmarks (fully automated)

```bash
./benchmark_runner.sh
```

This will:

* Sequentially start each framework server
* Run a high-load test using:

  ```bash
  wrk -t8 -c1000 -d60s -s post.lua http://localhost:3000/process
  ```
* Kill the server
* Save results in `results/`
* Generate `benchmark_dashboard.html`

## 📁 Project Structure

```
backend-benchmark/
├── <framework>/         # One folder per framework
│   └── install.sh       # Install dependencies of the framework (optional)
│   └── start.sh         # Starts that framework's server
├── results/             # Raw wrk output per framework
│   └── results_summary.csv  # Parsed performance data
├── benchmark_dashboard.html  # Interactive HTML report
├── post.lua             # wrk load script
├── benchmark_presetup.sh  # Install all dependencies
├── benchmark_runner.sh  # Run benchmarks
└── parse_html.py        # Parses wrk results into charts
```

## 📈 What You Get

After running the benchmark, you'll get:

* A fully standalone **interactive HTML dashboard** (`benchmark_dashboard.html`)
* Auto-sorted **charts** using [Chart.js](https://www.chartjs.org/):
  * Requests per second
  * Average latency (ms)
  * Transfer rate (kB/sec)
* A **summary table** of all raw numbers
* A **system/environment report** (OS, CPU, RAM, date, benchmark command, runtime versions)
* No external dependencies — open the file offline in any browser

## 🧾 Benchmark Results

* **macOS** – M1 Pro (8-core), 16 GB RAM — [View dashboard (May 23, 2025)](https://yannick-burkard.eu.org/results_dashboard_20250523.html)


## 🤝 Contributing

Pull requests welcome! Add frameworks, improve charts, or enhance the automation. Feel free to fork this repository and submit a [pull request](https://github.com/Drarox/Backend-Benchmark/pulls) with your changes.

## 📄 License

MIT — use freely, modify openly, benchmark responsibly.

