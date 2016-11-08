from flask_sqlalchemy import SQLAlchemy

# Create the idea of our database through Flask-SQLAlchemy library
db = SQLAlchemy()


class Airport(db.Model):
    """airport by airport code"""

    __tablename__ = "airports"

    airport_code = db.Column(db.String(3), primary_key=True)
    airport_name = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(200), nullable=True)
    airport_lat = db.Column(db.Float, nullable=False)
    airport_long = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Airport airport_code=%s airport_name=%s airport_city=%s airport_lat=%s airport_long=%s>"
                % (self.airport_code, self.airport_name, self.airport_city, self.airport_lat, self.airport_long))


class User(db.Model):
    """user of the webapp"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    origin_airport_code = db.Column(db.String(3), db.ForeignKey("airports.airport_code"), nullable=False)

    def __repr__(self):

        return ("<User user_id=%s username=%s password=%s origin_airport_code=%s>"
                % (self.user_id, self.username, self.password, self.origin_airport_code))


class Saved_trip(db.Model):
    """trip saved by user"""

    __tablename__ = "saved_trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.flight_id"), nullable=False)
    lodging_id = db.Column(db.Integer, db.ForeignKey("lodgings.lodging_id"), nullable=False)

    flight = db.relationship('Flight')
    lodging = db.relationship('Lodging')
 

    def __repr__(self):

        return ("<Saved_trip trip_id=%s user_id=%s flight_id=%s lodging_id=%s>"
                % (self.trip_id, self.user_id, self.flight_id, self.lodging_id))


class Flight(db.Model):
    """flight info in a saved trip"""

    __tablename__ = "flights"

    flight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    departure_airport = db.Column(db.String(3), db.ForeignKey("airports.airport_code"), nullable=False)
    destination_airport = db.Column(db.String(3), db.ForeignKey("airports.airport_code"), nullable=False)
    carrier = db.Column(db.String(50), nullable=False)
    outbond_departure_time = db.Column(db.String(50), nullable=False)
    outbond_arrival_time = db.Column(db.String(50), nullable=False)
    inbond_departure_time = db.Column(db.String(50), nullable=False)
    inbond_arrival_time = db.Column(db.String(50), nullable=False)
    flight_price = db.Column(db.String(50), nullable=False)

    def __repr__(self):


        return ("<Flight flight_id=%s departure_airport=%s destination_airport=%s" + 
                "carrier=%s outbond_departure_time=%s outbond_arrival_time=%s inbond_departure_time=%s inbond_arrival_time=%s flight_price=%s >"
                % (self.flight_id, self.departure_airport, self.destination_airport, self.carrier, 
                   self.outbond_departure_time, self.outbond_arrival_time, self.inbond_departure_time, self.inbond_arrival_time, self.flight_price))


class Lodging(db.Model):
    """lodging info in a saved trip"""


    __tablename__ = "lodgings"

    lodging_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    airbnb_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable= True)
    picture_url = db.Column(db.String(150), nullable= True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):


        return ("<Lodging lodging_id=%s airbnb_id=%s address=%s picture_url=%s price=%s>"
                % (self.lodging_id, self.airbnb_id, self.address, self.picture_url, self.price))


 



################################################################################

#Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app"""

    # Configure to use our PostgreSQL database
 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    # Connect db to server when running

    from server import app
    connect_to_db(app)
    #db.create_all()
    print "Connected to DB."