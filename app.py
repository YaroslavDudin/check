from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {name}!"

@app.route("/debug")
def debug():
    return eval(request.args.get("expr", ""))  # Уязвимость

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)