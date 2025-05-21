const fastify = require("fastify")();

fastify.post("/process", async (request, reply) => {
  const numbers = request.body.numbers || [];
  const result = numbers.reduce((sum, x) => sum + x * x, 0);
  return { result };
});

fastify.listen({ port: 3000 });
