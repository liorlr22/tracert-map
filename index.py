from getMap import main
from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/iframe")
def iframe():
    return render_template("map.html")


@app.route("/trace", methods=["POST"])
def trace():
    url = request.form["website"]
    main(url)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
