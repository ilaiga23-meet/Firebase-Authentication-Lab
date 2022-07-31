from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDNNi-ziz--jDOzLBHMPHcGVR2pdNyJy-8",
  "authDomain": "fir-lab-61e05.firebaseapp.com",
  "projectId": "fir-lab-61e05",
  "storageBucket": "fir-lab-61e05.appspot.com",
  "messagingSenderId": "1049268497596",
  "appId": "1:1049268497596:web:229eae0a9454bc655634b9",
  "measurementId": "G-NJF4MZW5GG",
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error  =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")
@app.route('/signout', methods=['GET', 'POST'])
def signout():
    return render_template("signin.html")


if __name__ == '__main__':
    app.run(debug=True)