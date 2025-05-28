#!/bin/bash
# Sequentially benchmarks all frameworks by running each server's start.sh

mkdir -p results/raw

# Ordered list of framework folders
FRAMEWORKS=(
  "flask"
  "fastapi"
  "node-http"
  "node-express"
  "node-fastify"
  "nest-express"
  "nest-fastify"
  "bun"
  "bun-express"
  "bun-fastify"
  "bun-hono"
  "bun-elysia"
  "deno"
  "deno-express"
  "deno-fastify"
  "go-gin"
  "go-echo"
  "go-fiber"
  "go-native"
)

for name in "${FRAMEWORKS[@]}"; do
  echo "🔧 Starting $name..."
  cd $name
  ./start.sh &

  echo "⏳ Waiting for $name to be ready..."
  until curl -s -H 'Content-Type: application/json' -d '{"numbers":[1,2,3,4,5]}' -X POST http://localhost:3000/process > /dev/null; do sleep 0.5; done

  echo "🚀 Running wrk on $name..."
  wrk -t8 -c1000 -d60s -s ../post.lua http://localhost:3000/process > ../results/raw/$name.txt

  SERVER_PID=$(cat server.pid)
  echo "🛑 Killing $name (PID $SERVER_PID)"
  kill $SERVER_PID
  wait $SERVER_PID 2>/dev/null
  rm server.pid

  sleep 2
  cd ..

echo "✅ $name benchmark complete."
done

# Parsing results & create html file
echo "🔧 Parsing results & create html file..."
python3 parse_html.py

echo "✅ All frameworks benchmark complete."

if [ -x "$(command -v open)" ]; then
  open results/results_dashboard.html
fi
