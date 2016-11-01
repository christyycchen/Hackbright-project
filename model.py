from flask_sqlalchemy import SQLAlchemy

# Create the idea of our database through Flask-SQLAlchemy library
db = SQLAlchemy()




































################################################################################

#Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app"""

    # Configure to use our PostgreSQL database
 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travels'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    # Connect db to server when running

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."