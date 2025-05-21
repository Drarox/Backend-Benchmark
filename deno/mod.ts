Deno.serve({ port: 3000 }, async (req) => {
  if (req.method === "POST" && new URL(req.url).pathname === "/process") {
    const { numbers } = await req.json();
    const result = numbers.reduce((sum: number, x: number) => sum + x * x, 0);
    return new Response(JSON.stringify({ result }), {
      headers: { "Content-Type": "application/json" },
    });
  }
  return new Response("Not Found", { status: 404 });
});
