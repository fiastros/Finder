from flask import  Blueprint, Flask, redirect , url_for , render_template, request, session, flash, jsonify
from flask_login import login_required, current_user
from .models import Candidat_profil
from . import db
import json

views = Blueprint('views',__name__)

@views.route("/")
def home():
    return render_template("index.html",user = current_user)


@views.route("/description")
def description():
    return render_template("elements.html",user = current_user)


@views.route('/matching', methods = ["POST","GET"])
@login_required
def matching():  
    if request.method =="POST":
        cv = request.form.get("cv")
        
        if len(cv) < 1 or len(cv) > 10:
            flash("trop court votre mot !", category="fail")
        else:
            new_cv = Candidat_profil(cv=cv, image= cv, addresse=cv,code_postal=cv,
                                     lettre_motivation=cv, recommendation = cv,
                                     reponse_questionnaire=cv, user_id = current_user.id)
            db.session.add(new_cv)
            db.session.commit()
    return render_template("generic.html", user = current_user)


@views.route("/admin")
@login_required
def admin():
    return render_template("admin.html",user = current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    cv = json.loads(request.data)
    cv_id = cv["cv_id"]
    cv = Candidat_profil.query.get(cv_id)
    if cv :
        if cv.user_id == current_user.id:
            db.session.delete(cv)
            db.session.commit()
    
    return jsonify({})