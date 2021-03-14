from . import db
from flask_login import UserMixin
from sqlalchemy import func

class Candidat(db.Model,UserMixin):
    __tablename__ = "candidat_parent"
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    username = db.Column(db.String(10), unique =True) 
    email = db.Column(db.String(10))
    password = db.Column(db.String(10))
    naissance = db.Column(db.String(10))
    sexe = db.Column(db.String(10))
    compte = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    profil = db.relationship("Candidat_profil",uselist=False, backref="candidat_parent")
    
              
class Candidat_profil(db.Model,UserMixin):
    __tablename__ = "candidat_child"
    id = db.Column(db.Integer,primary_key = True)
    image = db.Column(db.String(10))
    addresse = db.Column(db.String(10))
    code_postal = db.Column(db.String(10)) 
    cv = db.Column(db.String(10))
    lettre_motivation = db.Column(db.String(10))
    recommendation = db.Column(db.String(10))
    reponse_questionnaire = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey("candidat_parent.id"))

class Entreprise(db.Model,UserMixin):
    __tablename__ = "entreprise_parent"
    id = db.Column(db.Integer,primary_key = True)
    nom = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(10))
    ville = db.Column(db.String(10))
    compte = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    profil = db.relationship("Entreprise_profil",uselist=False, backref="entreprise_parent")

class Entreprise_profil(db.Model,UserMixin):
    __tablename__ = "entreprise_child"
    id = db.Column(db.Integer,primary_key = True)
    siret = db.Column(db.String(10), unique=True)
    adresse = db.Column(db.String(10))
    code_postal = db.Column(db.String(10), unique =True) 
    annonce = db.Column(db.String(100))
    description = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey("entreprise_parent.id"))

class Admin(db.Model,UserMixin):
    __tablename__ = "admin_parent"
    id = db.Column("id",db.Integer,primary_key = True)
    username = db.Column(db.String(10),unique=True)
    email = db.Column(db.String(10))
    password = db.Column(db.String(10))
    compte = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())

