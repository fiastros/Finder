from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db= SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
        
    from .views import views
    from .auth import auth
    from .candidats import candidats

    app.register_blueprint(views, url_prefix="")
    app.register_blueprint(auth, url_prefix="")
    app.register_blueprint(candidats, url_prefix="/candidat")
    
    from .models import User,Candidat,Entreprise,Admin #, Candidat_profil ,Entreprise_profil,

    create_database(app) 
       
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "connectez-vous d'abord !"
    login_manager.login_message_category="info"
    login_manager.needs_refresh_message = (u"veuillez vous reconnecter s'il vous plaît")
    login_manager.needs_refresh_message_category= "info"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
    
      
def create_database(app):
    if not path.exists("website/"+DB_NAME):
        db.create_all(app=app)
        print("le modele de base de données a été crée")
