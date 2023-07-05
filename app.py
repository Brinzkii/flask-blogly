"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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


@app.route("/users/<int:id>/posts/new", methods=["GET"])
def show_post_form(id):
    user = User.query.get_or_404(id)
    return render_template("new-post-form.html", user=user)


@app.route("/users/<int:id>/posts/new", methods=["POST"])
def submit_post(id):
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, author_id=id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)

    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    post = Post.query.get(post_id)

    return render_template("edit-post-form.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.op.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")
