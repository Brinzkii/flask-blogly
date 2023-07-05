"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.String(),
        default="/static/profile-icon.jpg",
    )


class Post(db.Model):
    """Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False, unique=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.String, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    op = db.relationship("User", backref="posts")
