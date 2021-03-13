#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:52:04 2021

@author: loic
"""

from flask import Blueprint, render_template

second = Blueprint("second",__name__, static_folder="static", template_folder="templates")

@second.route("/home")
@second.route("/")
def home():
     return render_template("index.html")
