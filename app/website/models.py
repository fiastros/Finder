from . import db
from flask_login import UserMixin
from sqlalchemy import func


class User(db.Model,UserMixin):   
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key = True)  
    email = db.Column(db.String(20))
    password = db.Column(db.String(10))
    adresse = db.Column(db.String(20))
    ville = db.Column(db.String(20))
    code_postale = db.Column(db.String(10))
    compte = db.Column(db.String(20))
    
    type =db.Column(db.String(20))    
    __mapper_args__ = {'polymorphic_identity':"user",
                       'polymorphic_on':type}

class Candidat(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id") ,primary_key = True)
    __tablename__ = "candidat_parent"

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique =True) 

    naissance = db.Column(db.String(20))
    sexe = db.Column(db.String(20))
    image = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default = func.now())

    # profil = db.relationship("Candidat_profil",uselist=False, backref="candidat_parent")
    
    __mapper_args__ = {'polymorphic_identity':'candidat'}
                  
# class Candidat_profil(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key = True)
#     __tablename__ = "candidat_child"
    
#     cv = db.Column(db.String(20))
#     lettre_motivation = db.Column(db.String(20))
#     recommendation = db.Column(db.String(20))
#     reponse_questionnaire = db.Column(db.String(20))
#     date = db.Column(db.DateTime(timezone=True), default = func.now())
#     user_id = db.Column(db.Integer,db.ForeignKey("candidat_parent.id"))
    

class Entreprise(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id") ,primary_key = True)
    __tablename__ = "entreprise_parent"
    username = db.Column(db.String(20), unique =True) 

    nom = db.Column(db.String(20),unique=True)
    siret = db.Column(db.String(20))
    description = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default = func.now())

    # profil = db.relationship("Entreprise_profil",uselist=False, backref="entreprise_parent")
    
    __mapper_args__ = {'polymorphic_identity':'entreprise'}

    

# class Entreprise_profil(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key = True)
#     __tablename__ = "entreprise_child"

#     annonce = db.Column(db.String(100))
#     date = db.Column(db.DateTime(timezone=True), default = func.now())
#     user_id = db.Column(db.Integer,db.ForeignKey("entreprise_parent.id"))


class Admin(User):
    id = db.Column("id",db.Integer,db.ForeignKey("user.id") ,primary_key = True)
    username = db.Column(db.String(20), unique =True) 
    date = db.Column(db.DateTime(timezone=True), default = func.now())


    __tablename__ = "admin_parent"
    __mapper_args__ = {'polymorphic_identity':'admin'}