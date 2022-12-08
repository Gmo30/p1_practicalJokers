"""
Practical Jokers
Softdev P01
2022-12-07
time spent: 3 hours
"""

from flask import Flask, render_template, request
app = Flask(__name__) 

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if(request.method == "GET"):
        return render_template( 'login.html' ) #displays the login page

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(request.method == "GET"):
        return render_template('register.html')  #displays register page
    else:
        return render_template("play.html") #play will be the home page

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()