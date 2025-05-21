const http = require("http");

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/process") {
    let body = "";
    req.on("data", chunk => body += chunk);
    req.on("end", () => {
      const data = JSON.parse(body);
      const numbers = data.numbers || [];
      const result = numbers.reduce((sum, x) => sum + x * x, 0);
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ result }));
    });
  }
});

server.listen(3000);
