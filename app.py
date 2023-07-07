"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "password"

connect_db(app)


@app.route("/")
def show_home():
    return render_template("base.html")


@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_new_form():
    return render_template("new-user-form.html")


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
    return render_template("edit-user-form.html", user=user)


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
    tags = Tag.query.all()
    return render_template("new-post-form.html", user=user, tags=tags)


@app.route("/users/<int:id>/posts/new", methods=["POST"])
def submit_post(id):
    req = request.form
    title = req["title"]
    content = req["content"]

    print(req.getlist("tag"))

    new_post = Post(title=title, content=content, author_id=id)

    db.session.add(new_post)
    db.session.commit()

    for t in req.getlist("tag"):
        post_tag = PostTag(post_id=new_post.id, tag_id=int(t))

        db.session.add(post_tag)
        db.session.commit()

    return redirect(f"/users/{id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)

    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    post = Post.query.get(post_id)
    all_tags = Tag.query.all()
    current_tags = []

    for tag in post.tags:
        current_tags.append(tag.id)

    return render_template(
        "edit-post-form.html", post=post, all_tags=all_tags, current_tags=current_tags
    )


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content
    update_tags(post_id, request.form.getlist("tag"), post.tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


def update_tags(post_id, selected_tags, applied_tags):
    post_tags = []

    # Check for tags that were removed
    for tag in applied_tags:
        # Grab tag ID from model for easy searching
        post_tags.append(tag.id)
        if str(tag.id) not in selected_tags:
            rem_tag = PostTag.query.filter_by(post_id=post_id, tag_id=tag.id).one()

            db.session.delete(rem_tag)
            db.session.commit()

    # Check for tags that were added
    for tag in selected_tags:
        if int(tag) not in post_tags:
            add_tag = PostTag(post_id=post_id, tag_id=int(tag))

            db.session.add(add_tag)
            db.session.commit()


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.op.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/tags")
def show_tags():
    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template("tag_details.html", tag=tag)


@app.route("/tags/new")
def show_new_tag_form():
    return render_template("new-tag-form.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    name = request.form["name"]
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template("edit-tag-form.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    name = request.form["name"]
    tag = Tag.query.get(tag_id)
    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
