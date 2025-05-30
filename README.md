# Backend Benchmark

A fully automated benchmarking suite comparing popular backend frameworks (Python, Go, Node, Deno, Bun). It measures performance on a consistent JSON-processing route and outputs a standalone HTML dashboard with visual results.

## ⚡ What It Does

* Benchmarks dozens of frameworks across languages
* Measures Requests/sec, Latency, Transfer/sec
* Generates a zero-dependency HTML dashboard with charts + system info (`results_dashboard.html`)

## 📦 Frameworks Covered

- **Python**: Flask, FastAPI  
- **JavaScript Runtimes**:
  - **Node**: Node (native), Express, Fastify, NestJS (Express), NestJS (Fastify)  
  - **Bun**: Bun (native), Express, Hono, Elysia
  - **Deno**: Deno (native), Express, Hono
- **Go**: Gin, Echo, Fiber, Native `net/http`

## 🔬 Benchmark Scenario

### Route: `POST /process`
- Input JSON: `{ "numbers": [1, 2, 3, 4, 5] }`
- Task: Compute the sum of squares of the numbers
- Output JSON: `{ "result": 55 }`

Each framework is tested using:

```bash
wrk -t"$CORES" -c1000 -d60s -s post.lua http://localhost:3000/process
```

## 📁 Project Structure

```
backend-benchmark/
├── <framework>/         # One folder per framework
│   └── install.sh       # Install dependencies of the framework (optional)
│   └── start.sh         # Starts that framework's server
├── results/             # Results ouput folder
│   └── raw/             # Raw wrk output per framework
│   └── results_summary.csv  # Parsed performance data
│   └── results_dashboard.html  # Interactive HTML report
├── post.lua             # wrk load script
├── benchmark_presetup.sh  # Install all dependencies
├── benchmark_runner.sh  # Run benchmarks
└── parse_html.py        # Parses wrk results into charts
```

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
* Run a high-load test using [`wrk`](https://github.com/wg/wrk)
* Kill the server
* Save results in `results/`
* Generate `results_dashboard.html`

## 🐳 Run with Docker (No Host Dependencies)

Don't want to install Python, Node, Go, Deno, Bun, or wrk on your machine?
No problem: everything runs cleanly inside a container.
The Docker image installs all the prerequisites !

### ✅ One-Time: Build the Docker image

```bash
docker build -t backend-benchmark .
```

### 🚀 Run the full benchmark suite

```bash
docker run --rm -v "$PWD/results:/app/results" backend-benchmark
```

* Benchmarks all frameworks
* Generates the HTML dashboard
* Mounts results to your host in the `results/` folder


This lets you run the full suite **with zero host setup** and clean everything up with one `docker rmi`.

## 🧾 Benchmark Results

* **macOS** – M1 Pro (8-core), 16 GB RAM — [View dashboard (May 28, 2025)](https://yannick-burkard.eu.org/backend-benchmark/results_dashboard_macos_20250528.html)

* **macOS (Docker Desktop)** – M1 Pro (8-core), 8 GB RAM — [View dashboard (May 28, 2025)](https://yannick-burkard.eu.org/backend-benchmark/results_dashboard_macos_docker_20250528.html)

* **Ubuntu (Docker)** – Xeon D-1531 (6-core), 32 GB RAM — [View dashboard (May 28, 2025)](https://yannick-burkard.eu.org/backend-benchmark/results_dashboard_ubuntu1_docker_20250528.html)

* **Ubuntu** – Xeon D-1531 (6-core), 32 GB RAM — [View dashboard (May 30, 2025)](https://yannick-burkard.eu.org/backend-benchmark/results_dashboard_ubuntu1_20250530.html)

* **Ubuntu (Docker)** – AMD Ryzen 7 1700X (8-core), 24 GB RAM — [View dashboard (May 30, 2025)](https://yannick-burkard.eu.org/backend-benchmark/results_dashboard_ubuntu2_docker_20250530.html)

## 🤝 Contributing

Pull requests welcome! Add frameworks, improve charts, or enhance the automation. Feel free to fork this repository and submit a [pull request](https://github.com/Drarox/Backend-Benchmark/pulls) with your changes.

## 📄 License

MIT — use freely, modify openly, benchmark responsibly.

