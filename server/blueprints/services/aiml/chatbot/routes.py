from flask import Blueprint, render_template, request, jsonify
from blueprints.services.aiml.chatbot.service import ChatbotService

chatbot= Blueprint("chatbot_bp", __name__, url_prefix="/chatbot")


@chatbot.route("/")
def chatbot_page():
    return render_template("chatbot.html")


@chatbot.route("/get_response", methods=["POST"])
def chatbot_respond():
    try:
        data = request.get_json()
        reply = ChatbotService.respond(data)
        return jsonify({"response": reply})
    except Exception as e:
        print(" Chatbot Error:", e)
        return jsonify({"response": "⚠️ Something went wrong!"})
