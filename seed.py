"""Seed file to make sample data for pets db"""

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Create users
Dawson = User(first_name="Dawson", last_name="Bezehertny")
Hannah = User(first_name="Hannah", last_name="Bezehertny")
Tyler = User(first_name="Tyler", last_name="Nieto")

# Create posts
post_1 = Post(title="Test 1", content="This is a test post", author_id=1)
post_2 = Post(title="Test 2", content="This is a test post", author_id=2)
post_3 = Post(title="Test 3", content="This is a test post", author_id=3)

# Create tags
tag_1 = Tag(name="fun")
tag_2 = Tag(name="weird")
tag_3 = Tag(name="sports")

# Add users,posts and tags to session
db.session.add(Dawson)
db.session.add(Hannah)
db.session.add(Tyler)
db.session.add(post_1)
db.session.add(post_2)
db.session.add(post_3)
db.session.add(tag_1)
db.session.add(tag_2)
db.session.add(tag_3)

# Commit new pets to database
db.session.commit()
