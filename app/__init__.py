from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    # Register Blueprints
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
