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
GAME_STARTED = False

@app.route("/", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('play'))
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
    if 'username' in session:
        return redirect(url_for('play'))
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

@app.route("/play", methods=['GET', 'POST'])
def play():
    global GAME_STARTED
    deckid = get_deck_id()
    if 'username' not in session:
        GAME_STARTED = False #not sure if necessary
        return redirect(url_for('login'))
    if 'username' in session:
        pcardlist = player_hand()
        move = str(request.form.get('move'))
        print(move)
        if(move == "hit" and GAME_STARTED):
            new_card = draw1(deckid)
            add_player_card(new_card[0], new_card[1])
            pcardlist = player_hand()
            dcardlist = dealer_hand()
            add = sub_hand_ace_player(get_player_value(), num_ace_in_P())
            dval = display_card_list(dcardlist)
            pval = display_card_list(pcardlist)
            if(get_player_value() > 21):
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_player_value() == 21):
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            phandvalue = get_player_value()
            dhandvalue = get_dealer_value()
            if(add[0]):
                add_hand_ace_player(get_player_value(), num_ace_in_P(), add[1])
            return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
        if(move == "stand" and GAME_STARTED):
            while GAME_STARTED and get_dealer_value() < 17:
                pcardlist = player_hand()
                dcardlist = dealer_hand()
                add = sub_hand_ace_player(get_player_value(), num_ace_in_P())
                dval = display_card_list(dcardlist)
                pval = display_card_list(pcardlist)
                if(get_dealer_value() > 21):
                    GAME_STARTED = False
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
                elif(get_dealer_value() == 21):
                    GAME_STARTED = False
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
                elif(get_dealer_value() >= 17 and get_dealer_value() >= get_player_value()):
                    GAME_STARTED = False
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
                elif(get_dealer_value() >= 17 and get_dealer_value() < get_player_value()):
                    GAME_STARTED = False
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
                if(add[0]):
                    add_hand_ace_player(get_player_value(), num_ace_in_P(), add[1])
                new_card = draw1(deckid)
                add_dealer_card(new_card[0], new_card[1])
            pcardlist = player_hand()
            dcardlist = dealer_hand()
            dval = display_card_list(dcardlist)
            pval = display_card_list(pcardlist)
            if(get_dealer_value() > 21):
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_dealer_value() >= get_player_value()):
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_dealer_value() < get_player_value()):
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
        if(move == "new"):
            GAME_STARTED = True
            reset_dealercards()
            reset_playercards()
            cardtuple = draw2(deckid)
            add_player_card(cardtuple[0], cardtuple[1])
            add_player_card(cardtuple[2], cardtuple[3])
            pcardlist = player_hand()

            cardtuple2 = draw2(deckid)
            add_dealer_card(cardtuple2[0], cardtuple2[1])
            add_dealer_card(cardtuple2[2], cardtuple2[3])
            dcardlist = dealer_hand()

            dval = display_card_list(dcardlist)
            pval = display_card_list(pcardlist)
            phandvalue = get_player_value()
            dhandvalue = get_dealer_value()
            return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
        else:
            if(pcardlist[0] == 'None'):
                pcardlist = player_hand()
                dcardlist = dealer_hand()
                dval = display_card_list(dcardlist)
                pval = display_card_list(pcardlist)
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_player_value() > 21):
                if(pcardlist[0] != 'None'):
                    GAME_STARTED = False
                    dcardlist = dealer_hand()
                    dval = display_card_list(dcardlist)
                    pval = display_card_list(pcardlist)
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_player_value() == 21):
                if(pcardlist[0] != 'None'):
                    GAME_STARTED = False
                    dcardlist = dealer_hand()
                    dval = display_card_list(dcardlist)
                    pval = display_card_list(pcardlist)
                    phandvalue = get_player_value()
                    dhandvalue = get_dealer_value()
                    return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_dealer_value() >= 17 and get_dealer_value() >= get_player_value()):
                GAME_STARTED = False
                dcardlist = dealer_hand()
                dval = display_card_list(dcardlist)
                pval = display_card_list(pcardlist)
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Lose",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            if(get_dealer_value() >= 17 and get_dealer_value() < get_player_value()):
                dcardlist = dealer_hand()
                dval = display_card_list(dcardlist)
                pval = display_card_list(pcardlist)
                GAME_STARTED = False
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', message = "You Win",  card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)
            else:
                dcardlist = dealer_hand()
                dval = display_card_list(dcardlist)
                pval = display_card_list(pcardlist)
                phandvalue = get_player_value()
                dhandvalue = get_dealer_value()
                return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist, dval = dval, pval = pval, phandvalue = phandvalue, dhandvalue = dhandvalue)


@app.route("/test", methods=['GET', 'POST'])
def test():
    GAME_STARTED = False
    if 'username' not in session:
        return redirect(url_for('login'))
    else: #in session
        if(GAME_STARTED):
            return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist)
        else: #Game not started
            if(request.method == "GET"):
                deckid= get_deck_id()
                bothhands = get_both_hands(deckid)
                pcardlist = bothhands[0]
                dcardlist = bothhands[1]
                GAME_STARTED = True
            pcardlist = ['None','None','None','None','None','None','None','None','None','None','None','None', 0]
            dcardlist = pcardlist
            return render_template('play.html', card_list = pcardlist, card_list2 = dcardlist)




@app.route("/leaderboard")
def leaderboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    mon = leaderboard_setup()
    ey=player_leaderboard_setup()
    return render_template('leaderboard.html', mon = mon, ey=ey) 

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if(request.method == "POST"):
        country = request.form["country"]
        update_country(session['username'], country)
        return render_template('profile.html', username = session['username'], message = "Updated country")

    return render_template('profile.html', username = session['username'])

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()
