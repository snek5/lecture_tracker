import os

from flask import Flask, redirect, url_for
from flask_login import current_user

from app.config import config
from app.extensions import cache, csrf, db, login_manager
from app.models import User
from app.routes.auth import bp as auth_bp
from app.routes.dashboard import bp as dashboard_bp
from app.routes.seminar import bp as seminar_bp


def create_app(config_name=None):
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    cache.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(seminar_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='test').first():
            test_user = User(username='test', email='test@example.com')
            test_user.set_password('12345678')
            db.session.add(test_user)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    return app
