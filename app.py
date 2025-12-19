import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if "dataset" not in request.files:
            return "No file key found ❌"

        file = request.files["dataset"]

        if file.filename == "":
            return "No file selected ❌"

        filename = secure_filename(file.filename)
        save_path = os.path.join("uploads", filename)

        file.save(save_path)

        return f"File saved successfully 🎉<br>Saved as: {filename}"

    return render_template("upload.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/report")
def report():
    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)
