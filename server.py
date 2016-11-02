from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
import json

# import db classes and tables from model file
import model 

# import my functions from functions file
import functions



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# undefined variable in Jinja2 raises an error
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True



@app.route('/')
def index():
    """landing page"""

    if session.get("user_id"):
        return redirect('/home')
    else: 
        return render_template('index.html')


@app.route('login', methods=["POST"])
def login():

    input_username = request.form.get() #username 
    input_password = request.form.get() #password


    #if email in db, 
        #if password match
            #save user in session 
            return redirect('/home')
        #if password doesnt match 
            #flash password doesnt match message
            return redirect('/')
    #else:
        #flash username not found, please register
        return redirect('/')



@app.route('register', methods=["POST"])
def register():

    input_username = request.form.get() #username 
    input_password = request.form.get() #password
    input_user_airport = request.form.get() #airport ---how to reinforce this?

    #if username does not exist
        #write user into db
        #add user to session
        return redirect('/home')
    #else 
        #flash you already registered before, do you want to log in?
        return redirect('/')




@app.route('/home')
def homepage():
    """user homepage"""

    #after logeed in, get user data from database by user_id in session
    #display user saved trip

    return render_template('homepage.html')



@app.route('/search_result', methods=["POST"])
def search_result():
    """send requests to APIs and display results"""


    departure_airport =  #get user default_airport in db
    destination_airport = #pick an airport 

    input_departure_date = request.form.get()
    input_return_date =  request.form.get()

    #call the functions to send results to API and get results 
    
    #set variables

    return render_template('result_page.html', #pass variables in)



@app.route('/home/<int:trip_id>')
def saved_trip(trip_id):
    """dusplay saved trip with details"""

    #get trip info from db

    return render_template('saved_trip.html')



@app.route('/home/<int:trip_id>/delete', methods=["POST"])
def delete_trip(trip_id):
    """delete a saved trip"""

    #delete trop by id from db

    return redirect('/home')



    





















################################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    #runs app
    app.run()
