import { Elysia } from "elysia";

const app = new Elysia()
  .post("/process", async ({ body }) => {
    const numbers = body?.numbers ?? [];
    const result = Array.isArray(numbers)
      ? numbers.reduce((sum, n) => sum + n * n, 0)
      : 0;
    return { result };
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
