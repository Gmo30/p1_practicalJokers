"""
Practical Jokers
Softdev P01
2022-12-07
time spent: 8 hours
"""

from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from api import *
app = Flask(__name__) 
app.secret_key = b'foo'

@app.route("/", methods=['GET', 'POST'])
def login():
    if(request.method == "GET"):
        return render_template( 'login.html' ) #displays the login page
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']

        if(user_exists(username)):
            if(password != 0):
                if(check_pass(username, password)):
                    session['username'] = request.form['username']
                    #print("\nCookie stuff: " + str(session)+ "\n")
                    return redirect(url_for('play'))#this page displays play page
                else:
                    return render_template('login.html', message = "Password is incorrect")
            else:
                return render_template('login.html', message = "Fill in password field")
        else:
            return render_template('login.html', message = "User doesn't exist")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(request.method == "GET"):
        return render_template('register.html')  #displays register page
    else:
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        country = request.form['country']
        print(country)
        if(len(username) == 0):
                return render_template('register.html', message = "User is too short")
        if(user_exists(username)):
            #print(username)
            return render_template('register.html', message = "User already exists")
        else:
            if(len(password) == 0):
                return render_template('register.html', message = "Please enter password")
            if(password == password_confirm):
                add_user(username, password, country)
                return redirect(url_for('login')) #when you register, redirects you to login
            else:
                return render_template('register.html', message = "Passwords don't match")

@app.route('/logout')
def logout():
    session.pop('username', None)
    print("\nPopped the cookie\n")
    login_status = False
    return redirect(url_for('login'))

@app.route("/play")
def play():
    if 'username' not in session:
        return redirect(url_for('login'))
    deckid = get_deck_id()
    cardlist = ["null","null","null","null","null",cardtuple[1],"null","null","null","null","null","null",]
    return render_template('play.html', message = joke(), card_list = cardlist)  

@app.route("/leaderboard")
def leaderboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('leaderboard.html')

@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()
