"""Message model tests."""

import os
from datetime import datetime
from unittest import TestCase

from models import db, User, Message, Follows
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


class MessageModelTestCase(TestCase):
    """Test the model for messages. """

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        user = User(
            email="test@test.com",
            username="testuser",
            password=bcrypt.generate_password_hash("HASHED_PASSWORD").decode('UTF-8'),
        )

        self.user = user

        db.session.add(user)
        db.session.commit()

        message = Message(
            text = "test message",
            # timestamp = test_time,
            user_id = user.id
        )

        self.message = message

        db.session.add(message)
        db.session.commit()
    
    
    def test_message_model(self):
        """Does basic message model work?"""

        # Message should have all attributes
        self.assertEqual(type(self.message.id), int)
        self.assertEqual(self.message.text, 'test message')
        self.assertEqual(self.message.user_id, self.user.id)