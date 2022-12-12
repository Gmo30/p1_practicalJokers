"""
Practical Jokers
Softdev P01
2022-12-07
time spent: 8 hours
"""

from flask import Flask, render_template, request, redirect, url_for
from db import *
from api import *
app = Flask(__name__) 

@app.route("/", methods=['GET', 'POST'])
def login():
    if(request.method == "GET"):
        return render_template( 'login.html' ) #displays the login page
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        #print(password)
        if(user_exists(username)):
            if(password != 0):
                if(check_pass(username, password)):
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
        if(len(username) == 0):
                return render_template('register.html', message = "User is too short")
        if(user_exists(username)):
            #print(username)
            return render_template('register.html', message = "User already exists")
        else:
            if(len(password) == 0):
                return render_template('register.html', message = "Please enter password")
            if(password == password_confirm):
                #add_user function needed
                return redirect(url_for('login')) #when you register, redirects you to login
            else:
                return render_template('register.html', message = "Passwords don't match")

@app.route("/play")
def play():
    return render_template('play.html', message = joke())  

@app.route("/leaderboard")
def leaderboard():
    return render_template('leaderboard.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()