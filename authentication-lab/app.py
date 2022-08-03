from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime
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
  "databaseURL": "https://fir-lab-61e05-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
@app.route('/add_like')
def add_like(tweet):
    tweet['likes'] += 1
    return tweet['likes']
    #save it to the db #

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
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password": password, "full_name": full_name, "username": username, "bio": bio}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error  =""
    if request.method == 'POST':
        title = request.form['title']
        discription = request.form['discription']
        today = datetime.now()
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        try:
            tweet = {"title": title, "discription": discription, 'time': today, "likes": 0}
            db.child("Tweet").child(login_session['user']['localId']).push(tweet)
            all_tweets2 = db.child("Tweet").child(login_session['user']['localId']).get().val().values()
            return render_template("all_tweets.html", all_tweets2 = all_tweets2)
        except:
           error = "Authentication failed"
           print(error)
    return render_template("add_tweet.html")
@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return render_template("signin.html")
if __name__ == '__main__':
    app.run(debug=True)