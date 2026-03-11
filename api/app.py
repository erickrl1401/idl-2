from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

from api.config import Config
from api.routes.auth_routes import auth_bp
from api.routes.cliente_routes import cliente_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS)

    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
    )
