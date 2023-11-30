from flask import Blueprint, jsonify, request


otherBP = Blueprint("other", __name__)


@otherBP.route("/", methods=["GET"])
def other():
    """Infer a prediction from a trained model."""
    return jsonify({"message": "Infer a prediction from a trained model."})
