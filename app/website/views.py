from flask import Flask, redirect , url_for , render_template
import os 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/description")
def description():
    return render_template("elements.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/matching')
def matching():
    return render_template("generic.html")



if __name__ == "__main__":
    app.run(debug = True)