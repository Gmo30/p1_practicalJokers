"""
Practical Jokers
Softdev P01
2022-12-07
time spent: 3 hours
"""

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__) 

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if(request.method == "GET"):
        return render_template( 'login.html' ) #displays the login page
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('play'))#this page displays play page

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(request.method == "GET"):
        return render_template('register.html')  #displays register page
    else:
        username = request.form['username'].lower()
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if(user_exists(username)):
        return render_template('register.html', message = "User already exists")
        else:
            if(password == password_confirm):
            return redirect(url_for('login')) #when you register, redirects you to login
            else:
                return render_template('register.html', message = "Passwords don't match")

@app.route("/play")
def play():
    return render_template('play.html')  


if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()