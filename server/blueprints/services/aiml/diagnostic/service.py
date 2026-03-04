from server.blueprints.services.aiml.diagnostic.model import DiagnosticModel

class DiagnosticService:

    @staticmethod
    def predict(data):
        symptoms = data.get("symptoms")

        if not symptoms or not isinstance(symptoms, list):
            return {"status": "error", "message": "Provide a valid list of symptoms"}

        if len(symptoms) < 3:
            return {"status": "error", "message": "Enter at least 2–3 symptoms"}

        # Build model input
        input_vector = DiagnosticModel.build_input_vector(symptoms)

        # Predict
        prediction, confidence = DiagnosticModel.predict(input_vector)

        # Get details
        details = DiagnosticModel.get_disease_details(prediction)

        return {
            "status": "success",
            "prediction": prediction,
            "confidence": round(confidence, 2),
            **details
        }
