from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>This is my home page!</p>"


if __name__ == "__main__":
    app.run(debug=True, port=5500)
