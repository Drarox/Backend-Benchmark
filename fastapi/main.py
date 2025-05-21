from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/process")
async def process(request: Request):
    body = await request.json()
    numbers = body.get("numbers", [])
    result = sum(x ** 2 for x in numbers)
    return {"result": result}
