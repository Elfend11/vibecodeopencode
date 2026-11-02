import os

from flask import Flask, jsonify


def create_app(test_config=None):
    """Create and configure the Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        DATABASE=os.path.join(app.instance_path, "lab_loan.db"),
        JSON_SORT_KEYS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    # SQLite database file lives in instance/ and is never served publicly.
    os.makedirs(app.instance_path, exist_ok=True)

    from app.database import init_app as init_database

    init_database(app)

    @app.errorhandler(404)
    def handle_not_found(error):
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "Endpoint atau data yang diminta tidak ditemukan.",
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "HTTP method tidak diizinkan untuk endpoint ini.",
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "Terjadi kesalahan pada server.",
                }
            ),
            500,
        )

    return app
