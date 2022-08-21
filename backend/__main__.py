from flask import render_template
from backend import create_app

app = create_app("dev")


@app.route("/", methods=["GET"])
def index():
    return render_template("vessel_trips.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
