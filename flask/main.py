from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    numbers = data.get("numbers", [])
    result = sum(x ** 2 for x in numbers)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(port=3000)
