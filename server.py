from jinja2 import StrictUndefined, Template
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask.ext.scss import Scss
from pprint import pprint
import json

# import db classes and tables from model file
from model import connect_to_db, db, Airport, User, Saved_trip, Flight, Lodging, City_img

# import functions from functions file
import functions

#import random to choose a random city
import random

#import datetime from datetime module
from datetime import datetime
import pytz
from dateutil.parser import parse

app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# undefined variable in Jinja2 raises an error
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True



@app.route('/')
def index():
    """landing page with login and register options"""

    #get list for user default airport dropdown
    airport_tuple_list = db.session.query(Airport.airport_code, Airport.airport_name).all()    
    airport_tuple_list.sort()


    #If user id in browser session, redirect to home page, if not, shows page for login and register. 
    if session.get("user_id"):
        return redirect('/home')
    else: 
        return render_template('index.html', airport_tuple_list=airport_tuple_list)


@app.route('/login', methods=["POST"])
def login():
    """log in route for registered user"""

    #get username and password from login form
    input_username = request.form.get("login-username")
    input_password = request.form.get("login-password")

    #check user info against database, flash appropriate messages
    if User.query.filter(User.username==input_username).first():
        login_user = User.query.filter(User.username==input_username).one()
        if login_user.password == input_password:
            session["user_id"]=login_user.user_id
            return redirect('/home')

        else:
            flash("Oops, wrong password!")
            return redirect('/')
    else:
        flash("Username is not found. Do you want to register?")
        return redirect('/')



@app.route('/register', methods=["POST"])
def register():

    #get user info from the registration form 
    input_username = request.form.get("register-username")
    input_password = request.form.get("register-password") 
    input_user_airport = request.form.get("user-airport")

    #check if user already existed in database
    if not User.query.filter(User.username==input_username).first():
        
        #instantiate user and add to db
        user = User(username=input_username,
                    password= input_password,
                    origin_airport_code=input_user_airport)
        db.session.add(user)
        db.session.commit()

        #add user in browser session
        session["user_id"]=User.query.filter(User.username==input_username).one().user_id
        flash("Welcom! Let's get you a vacation!!!")
        return redirect('/home')
    
    else: 
        flash("Username already exists. Pick another one or log in!")
        return redirect('/')



@app.route('/home')
def homepage():
    """user homepage"""

    #make sure user already logged in 
    if not session.get("user_id"):
        return redirect('/')

    print "this is user id in session **** ", session["user_id"]

    #if user has saved trips, display them
    if Saved_trip.query.filter(Saved_trip.user_id==session["user_id"]).first():
        user_saved_trips = Saved_trip.query.filter(Saved_trip.user_id==session["user_id"]).all()

    else:  
        user_saved_trips = None
        

    return render_template('homepage.html', saved_trip=user_saved_trips)


@app.route('/search_result', methods=["POST"])
def search_result():
    """send requests to APIs and display results"""

    if not session.get("user_id"):
        return redirect('/')

    #get the departure airport from user data
    user_airport= User.query.filter(User.user_id==session["user_id"]).one()

    #get the airport code
    departure_airport = user_airport.origin_airport_code
    
    #get all airports from db
    airport_list = db.session.query(Airport.airport_code).all()
    
    #remove user's departure airport
    airport_list.remove((departure_airport,))
    
    #get a random airport and the city associated with it 
    destination_airport = random.choice(airport_list)[0]
    destination_city = db.session.query(Airport.city).filter(Airport.airport_code==destination_airport).one()


    print "DEP AIPORT", departure_airport
    print "DES AIRPORT", destination_airport
    print "DES CITY", destination_city

    #get lat and long for both departure and destination airports 
    dep_airport = Airport.query.filter(Airport.airport_code==departure_airport).one()
    des_airport = Airport.query.filter(Airport.airport_code==destination_airport).one()
    dep_lat = dep_airport.airport_lat
    dep_long = dep_airport.airport_long
    des_lat = des_airport.airport_lat
    des_long = des_airport.airport_long

    #send request to google maps api
    map_result = functions.request_google_maps(dep_lat, dep_long, des_lat, des_long)


    #get user input dates
    input_departure_date = request.form.get("input-departure-date")
    input_return_date = request.form.get("input-return-date")

    

    #get flight info
    flight_response_dict= functions.request_QPX(departure_airport, destination_airport, input_departure_date,input_return_date)
    
    flight_info_dict = functions.parse_QPX(flight_response_dict)

    #get lodging info
    lodging_response_dict = functions.request_Airbnb(destination_city, input_departure_date, input_return_date)
    lodging_info_dict = functions.parse_Airbnb(lodging_response_dict)

    #get the ids associated with that flight and lodging
    current_flight_id = functions.get_flight_id(flight_info_dict)
    current_lodging_id = functions.get_lodging_id(lodging_info_dict)

    #combine all info into one dictionary to pass to jinja template
    flight_info_dict.update(lodging_info_dict)
    flight_info_dict["current_lodging_id"]=current_lodging_id
    flight_info_dict["current_flight_id"]=current_flight_id
    

    return render_template('result_page.html',
                            map_result=map_result,
                             **flight_info_dict )



@app.route('/savetrip', methods=["POST"])
def save_trip():
    """save trip into db, return the saving status"""

    #save the trip into database with ids for user, trip, flight and lodging
    current_user_id=session["user_id"]
    current_flight_id = request.form.get("current_flight_id")
    current_lodging_id = request.form.get("current_lodging_id")


    save_result = functions.save_trip_to_db(current_flight_id, current_lodging_id, current_user_id) 

    return save_result



@app.route('/home/<int:trip_id>')
def saved_trip(trip_id):
    """dusplay saved trip with details"""
    
    #get the trip info from database
    trip_details=Saved_trip.query.filter(Saved_trip.trip_id==trip_id).first()

    #get the destination city name
    destination_airport = trip_details.flight.destination_airport
    destination_city = db.session.query(Airport.city).filter(Airport.airport_code==destination_airport).one()[0]
    
    #get lat and long for both departure and destination airports 
    dep_airport = Airport.query.filter(Airport.airport_code==trip_details.flight.departure_airport).one()
    des_airport = Airport.query.filter(Airport.airport_code==trip_details.flight.destination_airport).one()
    dep_lat = dep_airport.airport_lat
    dep_long = dep_airport.airport_long
    des_lat = des_airport.airport_lat
    des_long = des_airport.airport_long


    #send request to google maps api
    map_result = functions.request_google_maps(dep_lat, dep_long, des_lat, des_long)

    #show flash message if the trip is expired
    departure_datetime = parse(trip_details.flight.outbound_departure_time)
    if departure_datetime < datetime.utcnow().replace(tzinfo=pytz.UTC):
        flash("Your trip is expired!")

    return render_template('saved_trip.html',
                         trip_details=trip_details,
                        destination_city=destination_city,
                        map_result=map_result)



@app.route('/home/<int:trip_id>/delete', methods=["POST"])
def delete_trip(trip_id):
    """delete a saved trip and rediret back to homepage"""

    #delete trip info from saved_trips table
    Saved_trip.query.filter(Saved_trip.trip_id==trip_id).delete()
    db.session.commit()

    return redirect('/home')


@app.route('/logout')
def logout():
    """Log out user and flash confirmation message"""

    #delete user id from browser session
    del session["user_id"]
    flash("You've been logged out successfully. Have a nice vacation!")

    return redirect('/')



@app.route('/view-city/<destinationcity>')
def view_city(destinationcity):
    """display city gallery"""
    print destinationcity

    airport_code = db.session.query(Airport.airport_code).filter(Airport.city==destinationcity).first()[0]

    print airport_code

    if City_img.query.filter_by(city_airportcode=airport_code).first():
        img_list = db.session.query(City_img.img_title, City_img.img_url).filter_by(city_airportcode=airport_code).all()
    else:
        img_list = None


    return render_template('view_city.html', destinationcity=destinationcity, img_list=img_list)




################################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    Scss(app, static_dir='static', asset_dir='static/assets')

    #runs app
    app.run(host="0.0.0.0")
