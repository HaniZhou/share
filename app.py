from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(64)

    from main import view
    app.register_blueprint(view)

    return app


if __name__ == "__main__":
    atc = create_app()
    atc.run(host="0.0.0.0", port=80)
