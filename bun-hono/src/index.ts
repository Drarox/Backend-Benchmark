import { Hono } from 'hono';

const app = new Hono();

app.post("/process", async (c) => {
  const { numbers = [] } = await c.req.json();
  const result = Array.isArray(numbers)
    ? numbers.reduce((sum, n) => sum + n * n, 0)
    : 0;
  return c.json({ result });
});

export default app
