# I'm Feeling Lucky 


I’m Feeling Lucky is a trip generator that searches for flights and Airbnb listings for users.
This search engine provides information regarding flight options and Airbnb listings based on entered criteria.  I’m Feeling Lucky enables users to set default departure airports, search trips, save trips for later, view or delete saved trips, and view photos of the destinations. I’m Feeling Lucky is great for people who love and want to travel. Planning trips is never easier!


## Features

User login/register page

User homepage - Search a new trip or view previous saved trips

Search Result - A flight and an Airbnb information for a trip

City Gallery - get a glimpse of the City



## Installing


Clone this repo:

```
https://github.com/christychen126/Hackbright-project
```

Create virtual environment on your laptop, inside a directory:

```
virtualenv env
source env/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

Get secret keys for Google Flights API, Google Maps API and Airbnb API, and save it to secrets.sh:

```
export QPX_KEY= "Your Key Goes Here"
export Airbnb_KEY= "Your Key Goes Here"
export Google_maps_KEY= "Your Key Goes Here"
```

Set up your database and seed city images:

```
python model.py
python seed.py
```

Start running your server:

```
python server.py
```

Open up your browser and navigate to:

```
 'localhost:5000/'
```

Have a nice trip!  :airplane:



## Built With                   


##### Backend

[Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), [PostgreSQL](https://www.postgresql.org/)

##### Frontend

JavaScript, HTML, CSS, [jQuery](https://jquery.com/), AJAX, [Jinja2](http://jinja.pocoo.org/docs/dev/)

##### APIs

[Google Flights API](https://developers.google.com/qpx-express/), [Google Maps API](https://developers.google.com/maps/), [The Unofficial Airbnb API](http://airbnbapi.org/)


## Version 2.0 Coming Up 

- **User Preferences:** Allow users to add preferred airlines, cabin, flght stops
- **City Guide:** Add city information, attractions, and tours.
- **Password hashing:** Passwords will be hashed before being saved in DB
- **Book Flight Link:** Direct users to airline websites
- **City Filter:** Allow users to filter city by city features and activities


