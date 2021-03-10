from flask import Flask, redirect , url_for , render_template

#ps -fA | grep python
#kill 3529  -> --port=43159

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)