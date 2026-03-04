from flask import Blueprint, render_template, request, jsonify
from blueprints.services.aiml.diagnostic.service import DiagnosticService

diagnostic = Blueprint("diagnostic_bp", __name__, url_prefix="/diagnostic")

@diagnostic.route("/", methods=["GET"])
def page():
    return render_template("diagnostic.html")


@diagnostic.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        result = DiagnosticService.predict(data)
        return jsonify(result), 200

    except Exception as e:
        print("Diagnostic Prediction Error:", e)
        return jsonify({"status": "error", "message": "Server Error"}), 500
