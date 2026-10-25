import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load local .env (if standalone repo) or root .env (if in project pipl)
local_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
if os.path.exists(local_env):
    load_dotenv(local_env)
elif os.path.exists(root_env):
    load_dotenv(root_env)

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates')),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')),
    )

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'admin-panel-secret-key-pipl-2024')
    app.config['SESSION_COOKIE_NAME'] = 'admin_session'
    app.config['REMEMBER_COOKIE_NAME'] = 'admin_remember_token'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    from datetime import timedelta
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # Database configuration (PostgreSQL Supabase / MySQL / SQLite)
    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        default_sqlite = 'sqlite:////tmp/database.db'
    else:
        default_sqlite = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'database.db')

    db_url = os.getenv('DATABASE_URL', default_sqlite)
    if db_url:
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        elif db_url.startswith('postgresql://'):
            db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu.'

    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.complaints import complaints_bp
    from backend.routes.users import users_bp
    from backend.routes.reports import reports_bp
    from backend.routes.settings import settings_bp
    from backend.routes.about import about_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(about_bp)

    @app.route('/')
    def root():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    # Serve user attachments & avatars
    root_uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'static', 'uploads'))
    admin_uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static', 'uploads'))
    tmp_uploads_dir = '/tmp/uploads'

    @app.route('/static/uploads/<path:filename>')
    def serve_shared_static_uploads(filename):
        # Cek /tmp dulu (Vercel serverless writable dir)
        tmp_path = os.path.join(tmp_uploads_dir, filename)
        if os.path.exists(tmp_path):
            return send_from_directory(tmp_uploads_dir, filename)
        if os.path.exists(os.path.join(admin_uploads_dir, filename)):
            return send_from_directory(admin_uploads_dir, filename)
        if os.path.exists(os.path.join(root_uploads_dir, filename)):
            return send_from_directory(root_uploads_dir, filename)
        return send_from_directory(admin_uploads_dir, filename)

    @app.route('/uploads/<path:filename>')
    def serve_shared_uploads(filename):
        tmp_path = os.path.join(tmp_uploads_dir, filename)
        if os.path.exists(tmp_path):
            return send_from_directory(tmp_uploads_dir, filename)
        if os.path.exists(os.path.join(admin_uploads_dir, filename)):
            return send_from_directory(admin_uploads_dir, filename)
        if os.path.exists(os.path.join(root_uploads_dir, filename)):
            return send_from_directory(root_uploads_dir, filename)
        return send_from_directory(admin_uploads_dir, filename)

    # Initialize tables and seed default admin account safely
    try:
        with app.app_context():
            db.create_all()
            from backend.models import Admin
            existing_admin = Admin.query.filter(
                (Admin.username == 'admin') | (Admin.email == 'admin@universitaspahlawan.ac.id')
            ).first()
            if not existing_admin:
                admin = Admin(
                    name='Administrator Utama',
                    email='admin@universitaspahlawan.ac.id',
                    username='admin',
                    role='superadmin',
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
    except Exception as e:
        print(f"Database initialization deferred/skipped: {e}")

    return app
