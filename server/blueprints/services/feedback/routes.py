from flask import Blueprint, request, jsonify, session
from blueprints.services.feedback.service import FeedbackService

feedback = Blueprint("feedback_bp", __name__, url_prefix="/feedback")

@feedback.route("/submit", methods=["POST"])
def submit_feedback():
    try:
        # User must be logged in
        if not session.get("logged_in"):
            return jsonify({
                "success": False,
                "message": "Please login to submit feedback"
            }), 401

        #  Block admin from submitting feedback
        role = session.get("role", "").lower()
        if role == "admin":
            return jsonify({
                "success": False,
                "message": "Admin cannot submit feedback"
            }), 403

        data = request.get_json()
        rating = data.get("rating")
        review = data.get("review", "").strip()

        # Basic validation
        if not rating or not review:
            return jsonify({
                "success": False,
                "message": "Rating and review are required"
            }), 400

        if len(review) > 60:
            return jsonify({
                "success": False,
                "message": "Review must be within 60 characters"
            }), 400

        # Session-based identity
        user_id = session.get("user_id")

        FeedbackService.store(
            user_id=user_id,
            rating=rating,
            review=review
        )

        return jsonify({
            "success": True,
            "message": "Feedback submitted successfully"
        }), 200

    except Exception as e:
        print("Feedback Error:", e)
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500
