from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      pw = request.form['pw']
      if pw == "password":
         return "access granted"
      else:
         return "access denied"
   return render_template('index.html')
