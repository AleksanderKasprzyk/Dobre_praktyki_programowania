from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/hello")
def hello():
    return jsonify({"hello": "world"}), 200

if __name__ == "__main__":
    app.run(debug=True)
