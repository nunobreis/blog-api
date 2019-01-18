from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.BlogpostView import blogpost_api as blogpost_blueprint

def create_app(env_name):
    # Create app

    # app initialization
    app = Flask(__name__)
    
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')

    @app.route('/')
    def index():
        return 'Welcome to the blog api'

    return app