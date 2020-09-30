"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        user1 = User(
            email="test@test.com",
            username="testuser",
            password=bcrypt.generate_password_hash("HASHED_PASSWORD").decode('UTF-8'),
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
        )
        self.user1 = user1
        self.user2 = user2
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        follow1 = Follows(
            user_being_followed_id = self.user1.id,
            user_following_id = self.user2.id,
            )
        self.follow1 = follow1
        db.session.add(follow1)
        db.session.commit()


    def tearDown(self):
        """ Cleans up."""
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.user1.messages), 0)
        self.assertEqual(len(self.user1.followers), 1) #update if necessary

    def test_repr_method(self):
        """ Does the __repr__ method work? """
        self.assertEqual(self.user1.__repr__(), f'<User #{self.user1.id}: testuser, test@test.com>')

    def test_is_following_true(self):
        """ Does is_following work when true? """

        self.assertEqual(self.user2.is_following(self.user1), True)

    def test_is_following_false(self):
        """ Does is_following work when false? """

        self.assertEqual(self.user1.is_following(self.user2), False)

    def test_is_followed_by_true(self):
        """ Does is_followed_by work when true? """

        self.assertEqual(self.user1.is_followed_by(self.user2), True)

    def test_is_followed_by_false(self):
        """ Does is_followed_by work when false? """

        self.assertEqual(self.user2.is_followed_by(self.user1), False)

    def test_user_signup(self):
        """ Does User.signup() work? """
        test_user = User.signup(username='test_signup', email='test_signup@gmail.com', password='hahaplaintextpassword', image_url='www.google.com')
        
        self.assertEqual(User.query.get(test_user.id), test_user)

    def test_user_signup_bad_input(self):
        """ Does User.signup() fail correctly with bad data? """
        good_test_signup = User.signup(username='duplicate_test_username', email='test_signup@gmail.com', password='hahaplaintextpassword', image_url='www.google.com')

        with self.assertRaises(IntegrityError):
            bad_test_signup = User.signup(username='duplicate_test_username', email='test_signup2@gmail.com', password='hahaplaintextpassword', image_url='www.google.com')

    def test_user_authenticate(self):
        """ Does User.authenticate() work? """
        username = 'testuser'
        password = 'HASHED_PASSWORD'
        user = User.query.get(self.user1.id)
        # print('@)(&$^)&*(%)(^&#)(*^$)(^%', user, username, user.password, password)
        # breakpoint()
        self.assertEqual(User.authenticate(username=username,
                                            password=password), user)

    def test_user_authenticate_false_username(self):
        """ Does User.authenticate() fail with wrong username """
        username = 'wrongusername'
        password = 'HASHED_PASSWORD'
        self.assertFalse(User.authenticate(username=username,
                                            password=password))

    def test_user_authenticate_false_password(self):
        """ Does User.authenticate() fail with wrong password? """
        username = 'testuser'
        password = 'WRONG_PASSWORD'
        self.assertFalse(User.authenticate(username=username,
                                            password=password))
    
