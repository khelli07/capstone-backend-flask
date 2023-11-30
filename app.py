from flask import Flask
from flask_cors import CORS
import os
import socket

from blueprints.infer.views import inferBP
from blueprints.other.views import otherBP


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(inferBP, url_prefix="/api/v1/infer")
    app.register_blueprint(otherBP, url_prefix="/api/v1/other")

    @app.route("/")
    def hello():
        html = "<h3>Hello {name}!</h3>" "<b>Hostname:</b> {hostname}<br/>"
        return html.format(
            name=os.getenv("NAME", "world"), hostname=socket.gethostname()
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
