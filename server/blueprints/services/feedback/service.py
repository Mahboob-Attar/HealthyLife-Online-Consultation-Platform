from server.blueprints.services.feedback.model import FeedbackModel

class FeedbackService:

    @staticmethod
    def store(user_id: int, rating: int, review: str):
        if not user_id:
            raise ValueError("User not authenticated")

        if not rating or not review:
            raise ValueError("Invalid feedback data")

        if len(review) > 60:
            raise ValueError("Review exceeds 60 characters")

        FeedbackModel.create(
            user_id=user_id,
            rating=rating,
            review=review
        )

        return True
