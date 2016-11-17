import unittest

from server import app
from model import db, connect_to_db
from flask import Flask, render_template, redirect, request, flash, session

class RouteTestsUserInSession(unittest.TestCase):
    """Tests routes when user in session"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        connect_to_db(app)
        with self.client.session_transaction() as session:
            session["user_id"] = 1

    def tearDown(self):
        pass


    def test_index(self):
        result = self.client.get("/", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Departure", result.data)


    def test_homepage(self):
        result = self.client.get("/home")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Departure", result.data)

    def test_viewcity(self):
        result = self.client.get("/view-city/Chicago")
        self.assertEqual(result.status_code, 200)
        self.assertIn("City Gallery of", result.data)

    def test_logout(self):
        self.client.get('/logout', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        assert "Pretty placeholder" in result.data

class RouteTestsUserNOTInSession(unittest.TestCase):
    """Tests routes when user not in session"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        connect_to_db(app)

    def tearDown(self):
        pass


    def test_index(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("I'm Feeling Lucky", result.data)


    def test_homepage(self):
        result = self.client.get("/home", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("I'm Feeling Lucky", result.data)

    def login(self, email, user_password):
        return self.client.post('/login', data=
            {"email":email,
            "user-password":user_password},
            follow_redirects=True)
        result = self.login('minyisme@gmail.com', 'abc123')
        self.assertEqual(result.status_code, 200)
        assert "minyisme" in result.data

    def test_user_registration(self):
        result = self.user_registration('minyisme@gmail.com', 'abc123', 'minyisme', 'SFO')
        self.assertEqual(result.status_code, 200)
        assert "Pretty placeholder" in result.data

class databaseTest(unittest.TestCase):
        """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_(self):
        """Test departments page."""

        result = self.client.get("/games")
        self.assertIn("Power Grid", result.data)





if __name__ == "__main__":
    unittest.main()

