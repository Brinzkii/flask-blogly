"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "password"

connect_db(app)


@app.route("/")
def show_home():
    return redirect("/users")


@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_new_form():
    return render_template("new-form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first = request.form["first"]
    last = request.form["last"]
    url = request.form["url"]
    print(url)

    if url == "":
        url = "/static/profile-icon.jpg"

    new_user = User(first_name=first, last_name=last, image_url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:id>")
def show_details(id):
    user = User.query.get_or_404(id)
    return render_template("details.html", user=user)


@app.route("/users/<int:id>/edit", methods=["GET"])
def show_edit_form(id):
    user = User.query.get_or_404(id)
    return render_template("edit-form.html", user=user)


@app.route("/users/<int:id>/edit", methods=["POST"])
def submit_edit(id):
    first = request.form["first"]
    last = request.form["last"]
    url = request.form["url"]
    user = User.query.get_or_404(id)

    if url == "":
        url = "/static/profile-icon.jpg"

    user.first_name = first
    user.last_name = last
    user.image_url = url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{id}")


@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
