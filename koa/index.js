const Koa = require("koa");
const Router = require("@koa/router");
const { bodyParser } = require("@koa/bodyparser"); 

const app = new Koa();
const router = new Router();

app.use(bodyParser());

router.post("/process", (ctx) => {
  const numbers = ctx.request.body.numbers || [];
  const result = numbers.reduce((sum, x) => sum + x * x, 0);
  ctx.body = { result };
});

app.use(router.routes());
app.use(router.allowedMethods());

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
