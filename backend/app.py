import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from werkzeug.exceptions import NotFound
from utils.response import success_response, error_response
import pandas as pd
from utils.file_utils import allowed_file, save_file
from core.cleaner import clean_dataframe
from core.store import save_dataset, get_dataset, clear_dataset
from flask_cors import CORS



app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})




def setup_logging(app):
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=1024 * 1024,
        backupCount=5
    )
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Logging is set up")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Ensure upload folder exists
    import os
    upload_folder = app.config.get("UPLOAD_FOLDER")

    if not upload_folder:
     raise RuntimeError("UPLOAD_FOLDER not set in Config")

    import os
    os.makedirs(upload_folder, exist_ok=True)

    setup_logging(app)

    # ---------------- HEALTH ----------------
    @app.route("/health", methods=["GET"])
    def health():
        app.logger.info("Health check called")
        return jsonify({
            "status": "success",
            "message": "Backend is running",
            "data": None
        })
    

    # ---------------- API: UPLOAD ----------------
    @app.route("/api/upload", methods=["POST"])
    def upload_file():
     if "file" not in request.files:
        return error_response("No file part in request", 400)

     file = request.files["file"]

     if file.filename == "":
        return error_response("No file selected", 400)

     if not allowed_file(file.filename):
        return error_response("Only CSV and XLSX files are allowed", 400)

     filename, file_path = save_file(file, app.config["UPLOAD_FOLDER"])
     app.logger.info(f"File saved: {filename}")

     # Read file safely
     try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path, encoding="latin1")
        else:
            df = pd.read_excel(file_path)
     except Exception:
        app.logger.exception("Failed to read uploaded file")
        return error_response("Unable to read the uploaded file", 400)

      # Clean data (THIS MUST BE OUTSIDE try/except)
     try:
        df = clean_dataframe(df)
     except Exception:
        app.logger.exception("Data cleaning failed")
        return error_response("Data cleaning failed", 500)

     # First 10 rows preview (after cleaning)
     preview_rows = df.head(10).to_dict(orient="records")

     return success_response(
        "File uploaded and processed successfully",
        {
            "dataset_id": filename,  # temporary id
            "filename": filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "preview_rows": preview_rows
        }
     )



    # ---------------- API: OVERVIEW ----------------
    @app.route("/api/overview", methods=["GET"])
    def overview():
     dataset_id = request.args.get("dataset_id")

     if not dataset_id:
        return error_response("dataset_id is required", 400)

     app.logger.info(f"Overview requested for dataset {dataset_id}")

     return success_response(
        "Dataset overview generated",
        {
            "dataset_id": dataset_id,
            "rows": 100,
            "columns": 5,
            "missing_values": {
                "col1": 2
            }
        }
     )



    # ---------------- API: ANALYSIS ----------------
    @app.route("/api/analysis", methods=["POST"])
    def analysis():
     payload = request.get_json()

     if not payload:
        return error_response("JSON body required", 400)

     dataset_id = payload.get("dataset_id")
     analysis_type = payload.get("analysis_type")

     if not dataset_id or not analysis_type:
        return error_response("dataset_id and analysis_type are required", 400)

     app.logger.info(f"Analysis requested for dataset {dataset_id}")

     return success_response(
        "Analysis completed",
        {
            "result_type": "table",
            "columns": ["category", "value"],
            "rows": [
                ["A", 10],
                ["B", 20]
            ]
        }
     )


    # ---------------- API: REPORT ----------------
    @app.route("/api/report", methods=["POST"])
    def report():
        app.logger.info("Report generation requested")
        return jsonify({
            "status": "success",
            "message": "Report generated",
            "data": {
                "download_url": "/downloads/report_dummy.pdf"
            }
        })

    # ---------------- GLOBAL ERROR HANDLER ----------------

        # ---------------- 404 HANDLER ----------------
    @app.errorhandler(404)
    def not_found(e):
        app.logger.warning("404 - Route not found")
        return jsonify({
            "status": "error",
            "message": "Route not found",
            "data": None
        }), 404


    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled exception occurred")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "data": None
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
