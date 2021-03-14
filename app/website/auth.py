from flask import  Blueprint, redirect , url_for , render_template, request, flash
from .models import Candidat,Entreprise
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
 
auth = Blueprint('auth',__name__)

@auth.route("/login", methods = ['POST',"GET"])
def login():
    if request.method =="POST":
        username = request.form.get("utilisateur")
        user_password =  request.form.get("mdp")
        
        found_user = Candidat.query.filter_by(username = username).first()
        if found_user  : 
            if check_password_hash(found_user.password,user_password) :
                login_user(found_user, remember=True)
                flash(f"vous êtes bien connecté {username}!", category="success")
                return redirect(url_for("views.matching"))
            else:
                flash("erreur de mot de passe!", category="fail")
        else:
            flash("ce compte n'existe pas", category="fail")
    return render_template("login.html")
        
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("vous êtes bien deconnete !")
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods = ["POST","GET"])
def signup():       
    if request.method =="POST":
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")
        email = request.form.get("email")
        username = request.form.get("utilisateur")
        user_password =  request.form.get("mdp")
        verif_password =  request.form.get("mdp_check")
        naissance  = request.form.get("naissance")
        sexe = request.form.get("sexe")
        compte = request.form.get("compte")

        #verification du username dans la base de données
        found_user = Candidat.query.filter_by(username = username).first() #TODO: y'a que le username qui est unique ici
         
        #verification des informations valides
        longueur_key = False
        for key in [first_name,last_name,email,username,user_password]:
            if len(key) > 10 :
                longueur_key = True
                break
            else :
                longueur_key = False
                
        if user_password != verif_password :
            flash("mots de passe differents", category ='fail')
        elif longueur_key :
            flash("10 charactères maximum !", category ="fail")        
        elif found_user : 
            flash(f"le username {username} est deja prit !", category ='fail')         
        else:
            new_user= Candidat(first_name=first_name,last_name=last_name,username=username,
                               naissance=naissance,sexe=sexe,compte=compte,
                               password =generate_password_hash(user_password, method="sha256") )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash(f"vous avez bien creer un compte {username}",category ='success')
            return redirect(url_for("views.matching"))
        
   
    return render_template("signup.html")
