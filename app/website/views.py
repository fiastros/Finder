from flask import Flask, redirect , url_for , render_template, request, session, flash

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/description")
def description():
    return render_template("elements.html")

@app.route("/login", methods = ['POST',"GET"])
def login():
    if request.method == "POST":
        username = request.form["utilisateur"]
        user_password =  request.form["mdp"]
        #verification des données dans la base de données
        
        #session
        session["username"] = username
        session["user_password"] = user_password
        
        return redirect(url_for("matching"))
    
    else:     
        if ("username" in session) and ("user_password" in session):
            return redirect( url_for("matching"))
        
        return render_template("login.html")

@app.route("/signup", methods = ["POST","GET"])
def signup():
    return render_template("signup.html")

@app.route("/logout")
def logout():
    [session.pop(key)  for key in ["username","user_password"] ]
    flash(" Vous êtes deconnecté !", "info")
    return redirect(url_for("login"))

@app.route('/matching', methods = ["POST","GET"])
def matching():
    if ("username" in session) and ("user_password" in session):
        username = session['username']
        user_password = session["user_password"]
    else:
        return redirect(url_for("login"))
        
    return render_template("generic.html")



if __name__ == "__main__":
    app.run(debug = True)