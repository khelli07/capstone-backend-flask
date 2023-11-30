from flask import Blueprint, jsonify, request


inferBP = Blueprint("infer", __name__)


@inferBP.route("/", methods=["POST"])
def infer():
    """Infer a prediction from a trained model."""
    return jsonify({"message": "Infer a prediction from a trained model."})
