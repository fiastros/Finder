#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 00:11:41 2021

@author: loic
"""

from flask import  Blueprint, Flask, redirect , url_for , render_template, request, session, flash, jsonify
from flask_login import login_required, current_user
from .models import Candidat_profil, Candidat
from . import db
import json

candidats = Blueprint('candidats',__name__)

@candidats.route("/personnelle")
@login_required
def home():
    if current_user.compte !="candidat":
        flash("vous n'êtes pas un candidat !",'fail')
        return redirect(url_for("views.matching"))
    return render_template("/candidat/personelle.html")
