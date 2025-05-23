const express = require("express");
const app = express();

app.use(express.json());

app.post("/process", (req, res) => {
  const numbers = req.body.numbers || [];
  const result = numbers.reduce((sum, x) => sum + x * x, 0);
  res.json({ result });
});

app.listen(3000);
