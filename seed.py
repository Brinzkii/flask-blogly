"""Seed file to make sample data for pets db"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Create pets
Dawson = User(first_name="Dawson", last_name="Bezehertny")
Hannah = User(first_name="Hannah", last_name="Bezehertny")
Tyler = User(first_name="Tyler", last_name="Nieto")

# Add new pets to session
db.session.add(Dawson)
db.session.add(Hannah)
db.session.add(Tyler)

# Commit new pets to database
db.session.commit()
