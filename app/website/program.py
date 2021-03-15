from flask import Flask, redirect , url_for , render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class users(db.Model):
    #TODO: rajouter une colonne type de compte : admin,candidat,entreprise
    _id = db.Column("id",db.Integer,primary_key = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(20)) 
    email = db.Column(db.String(20))
    password = db.Column(db.String(20))
    verif_password = db.Column(db.String(20))
    naissance = db.Column(db.String(20))
    sexe = db.Column(db.String(20))
    compte = db.Column(db.String(20))

    def __init__(self,first_name,last_name, username, email, password,verif_password,naissance,sexe,compte):
        self.first_name = first_name
        self.last_name =last_name
        self.username = username
        self.email = email
        self.password = password 
        self.verif_password = verif_password
        self.naissance = naissance
        self.sexe = sexe
        self.compte = compte

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
        #TODO
        
        found_user  = users.query.filter_by(username = username).first()
        if found_user:
            session["username"] = username
            
            #TODO: rediriger vers type de persone: admin, entreorise, candidat
            if username =="loco":
                session['admin'] = True
                flash(f"vous êtes connecté en tant qu'administrateur {username}")
                return redirect(url_for("admin"))
            else:
                flash(f" vous êtes bien connecté : {found_user.username}","info")
                return redirect(url_for("matching"))
        else:
            flash("votre compte n'existe pas, crée le !","error")
            return redirect(url_for("login"))       
    else:     
        if "username" in session:
            
            flash(f" vous êtes deja connecté : {session['username']}","info")
            return redirect( url_for("matching"))
        
        return render_template("login.html")

@app.route("/signup", methods = ["POST","GET"])
def signup():
    email = None 
    
    if request.method == "POST":

        username = request.form["utilisateur"]

        #verification 2 mot de passe
        #TODO: verifications mot de passe, et date  de nassaince (+18)
        
        #creation et/ou verification du compte crée
        #TODO: ameliorer les identifiants uniques
        found_user = users.query.filter_by(username = username).first()
        
        if found_user:
           # session["username"] = found_user.username
           flash(f"l'utilisateur {username} est deja prit !","error")
           return redirect(url_for("signup"))
           
        else:
            session["username"] = username
            
            db.session.add( users(*request.form.values()) )
            db.session.commit()
             
            flash(f"votre compte a bien été crée {session['username']}","info")
            return redirect(url_for("matching"))
        
    else:
        if "username" in session:
            flash(f"deconnectez vous d'abord : {session['username']}","info")
            return redirect(url_for("matching"))
        
        return render_template("signup.html")

@app.route("/logout")
def logout():
    if "username" in session :
        username = session['username']
      
        flash(f" Vous êtes deconnecté : {username}", "info")
        #[session.pop(key)  for key in ["username","user_password"] ]
        session.pop("username",None)
        session.pop("admin",None)
        
    else:
        flash("Vous êtes déja deconnecté !","info")    
    return redirect(url_for("login"))

@app.route('/matching', methods = ["POST","GET"])
def matching():
    

    if "username" in session:
        username = session['username']
        
    else:
        flash("Connectez vous d'abord !","info")
        return redirect(url_for("login"))
        
    return render_template("generic.html")
@app.route("/admin")

def admin():
    #TODO: permettre aux admins de supprimer la base de données
    # found_user = users.query.filter_by(username=username).delete()
    # db.commit()
    
    if ("username" in session) and ("admin" in session):
        username = session['username'] 
    else:
        flash("vous n'êtes pas admin !","info")
        return redirect(url_for("matching"))
        
    return render_template("admin.html", values = users.query.all(), admin = username)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)