# Backend Benchmark

This project benchmarks different backend frameworks for handling a simple JSON-processing POST route.

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

## 🧪 Benchmarking

Using [wrk](https://github.com/wg/wrk) with the provided `post.lua` script:

```bash
wrk -t8 -c1000 -d60s -s post.lua http://localhost:3000/process
```

## 📁 Structure

Each framework has its own folder inside the main directory. Run each individually to benchmark it.

## 🚀 Running

Each framework can be run with its corresponding language runtime.

### Python Flask
```bash
gunicorn -w 8 main:app -b :3000
```

### Python FastAPI
```bash
uvicorn main:app --port 3000
```

### Node (Native, Express, Fastify)
```bash
node index.js
```

### NestJS (Express, Fastify)
```bash
npm run build && npm run start:prod 
```

### Bun
```bash
bun index.ts
```

### Deno
```bash
deno run --allow-net mod.ts 
```

### Go (Native, Gin, Echo, Fiber)
```bash
go run main.go
```

---

