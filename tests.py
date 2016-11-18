"""tests for project"""


import unittest

from server import app
from model import db, connect_to_db, example_data
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


    def testIndex(self):
        result = self.client.get("/", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Departure", result.data)


    def testHomepage(self):
        result = self.client.get("/home")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Departure", result.data)

    def testViewcity(self):
        result = self.client.get("/view-city/Chicago")
        self.assertEqual(result.status_code, 200)
        self.assertIn("City Gallery of", result.data)

    def testLogout(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("logged out successfully", result.data)

class RouteTestsUserNOTInSession(unittest.TestCase):
    """Tests routes when user not in session"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def tearDown(self):
        pass


    def testIndexNotloggedin(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("I'm Feeling Lucky", result.data)


    def testHomepageNotloggedin(self):
        result = self.client.get("/home", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("I'm Feeling Lucky", result.data)


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
        #db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        #db.drop_all()

    def testLogin(self):
        result = self.client.post("/login",
                                    data={"login-username": "brucewayne100","login-password":"batman"},
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("logged in", result.data)

    def testLoginWrongPassword(self):
        result = self.client.post("/login",
                                    data={"login-username": "brucewayne100","login-password":"batman100"},
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("wrong password", result.data)

    def testRegistrationUserExist(self):
        result = self.client.post("/register", 
                                    data={"register-username": "brucewayne100", "register-password": "batman", "user-airport": "LAX" },
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Pick another", result.data)


    def testRegistrationUserNotExist(self):
        result = self.client.post("/register", 
                                    data={"register-username": "brucewayne101", "register-password": "batman", "user-airport": "LAX" },
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome", result.data)


################################################################################


if __name__ == "__main__":
    unittest.main()

