from app.routes.item_routes import bp as item_bp


def init_app(app):
    app.register_blueprint(item_bp)
