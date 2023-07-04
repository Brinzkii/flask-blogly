from unittest import TestCase
from app import app
from models import db, User

# Connect to test db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = True
app.config["TESTING"] = True

db.drop_all()
db.create_all()


class AppTestCase(TestCase):
    """Unit tests for Blogly app.py"""

    def setUp(self):
        """Add test user"""

        User.query.delete()

        user = User(first_name="Jane", last_name="Doe")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up db"""

        db.session.rollback()

    def test_show_home(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane", html)

    def test_show_new_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create a user", html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "Tom", "last": "Brady", "url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tom", html)
            self.assertIn("Brady", html)

    def test_show_details(self):
        with app.test_client() as client:
            user = User.query.one()
            resp = client.get(f"/users/{user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane", html)
            self.assertIn("Profile", html)
