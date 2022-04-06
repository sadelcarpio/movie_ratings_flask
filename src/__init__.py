from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# init SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(import_name=__name__)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../movie_ratings.sqlite'
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth as auth_blueprint
    from .movies import movies as movies_blueprint
    from .reviews import reviews as reviews_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(movies_blueprint, url_prefix='/movie')
    app.register_blueprint(reviews_blueprint, url_prefix='/review')
    return app
    
