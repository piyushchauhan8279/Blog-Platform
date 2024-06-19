# [ IMPORTED MODULES ]
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Integer, String, desc
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from app import create_app
from flask import flash, redirect, render_template, request, session, url_for

# creates an instance of the Flask app
app = create_app()
BLOGS_PER_PAGE = 4


# [ DATABASE CLASS ]
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)
userLogin = False


class User(db.Model):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    email = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(50), nullable=False)
    fullname = mapped_column(String(30), nullable=False)
    account_created = mapped_column(DateTime, default=db.func.current_timestamp())
    is_blog_publisher = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:

        return f"{self.id} {self.username} {self.email} {self.password} {self.fullname} {self.account_created}"


class Blog(db.Model):
    __tablename__ = "blog"
    blog_id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), nullable=False)
    blog_slug = mapped_column(String(100), unique=True, nullable=False)
    blog_title = mapped_column(String(100), unique=True, nullable=False)
    blog_content = mapped_column(String(2000), nullable=False)
    blog_likes = mapped_column(Integer, default=0)
    blog_date = mapped_column(DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"{self.blog_id} \n{self.username} \n{self.blog_slug} \n{self.blog_title} \n{self.blog_content} \n{self.blog_likes} \n{self.blog_date}"


class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = mapped_column(Integer, primary_key=True)
    blog_id = mapped_column(Integer, nullable=False)
    blog_comment = mapped_column(String(200), nullable=False)
    blog_comment_by_username = mapped_column(String(50), nullable=False)
    fullname = mapped_column(String(30), nullable=False)
    comment_date = mapped_column(DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"{self.blog_comment} \n{self.blog_comment_by_username} \n{self.fullname} \n{self.comment_date}"


# [ DATABASE FUNCTIONS ]
def add_blog(username, blog_title, blog_content):
    # Check if the user with the username already exists
    replaced_blog_title = "".join(
        letter for letter in blog_title if letter.isalnum() or letter == " "
    )
    blog_slug = replaced_blog_title.replace(" ", "_").lower()
    existing_blog = Blog.query.filter_by(blog_slug=blog_slug).first()
    if existing_blog is None:
        new_blog = Blog(
            username=username,
            blog_slug=blog_slug,
            blog_title=blog_title,
            blog_content=blog_content,
        )
        db.session.add(new_blog)
        db.session.commit()
        return f"blog '{blog_slug}' has been added"
    else:
        return f"blog '{blog_slug}' already exists in the database."


def get_blog_by_slug(blog_slug):
    existing_blog = Blog.query.filter_by(blog_slug=blog_slug).first()
    # Check if the blog with the blog_slug already exists
    if existing_blog is not None:
        return existing_blog
    else:
        return f"blog '{blog_slug}' does not exists in the database."


def add_user(username, email, password, fullname):
    # Check if the user with the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_user = User(
            username=username, email=email, password=password, fullname=fullname
        )
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        return f"user '{username}' has been added : {new_user}"
    else:
        return f"User '{username}' already exists in the database."


# make blog publisher
def make_user_blog_publisher_by_email(email):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        existing_user.is_blog_publisher = True
        db.session.commit()
        return f"User `{existing_user.username}` has been made blog publisher"
    return f"User does not exists!"


def is_user_blog_publisher(user_id):
    existing_user = User.query.filter_by(id=user_id).first()
    if existing_user is not None and existing_user.is_blog_publisher:
        return True
    return False


def delete_user_by_username(username):
    # Check if the user with the username EXISTS OR NOT
    user = User.query.filter_by(username=username).first()
    if user is None:
        return f"User `{username}` does not found in database"
    else:
        db.session.delete(user)
        # Commit the changes to the database
        db.session.commit()
        return f"User {user.username} has been deleted successfully : {user}"


def add_comment_by_username(username, blog_id, blog_comment):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        comment = Comment(
            blog_id=blog_id,
            blog_comment=blog_comment,
            blog_comment_by_username=username,
            fullname=user.fullname
        )
        db.session.add(comment)
        db.session.commit()
        return "comment added"
    else:
        return None


def add_comment_by_userid(userid, blog_id, blog_comment):
    user = User.query.filter_by(id=userid).first()
    if user is not None:
        comment = Comment(
            blog_id=blog_id,
            blog_comment=blog_comment,
            blog_comment_by_username=user.username,
            fullname=user.fullname
        )
        db.session.add(comment)
        db.session.commit()
        return "comment added"
    else:
        return None


# [ ROUTES ]
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call the associated function.
@app.route("/")
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    blogs = db.paginate(
        db.select(Blog).order_by(desc(Blog.blog_date)), page=1, per_page=BLOGS_PER_PAGE
    )
    last_page = list(blogs.iter_pages())[-1]
    return render_template(
        "home.html", blogs=blogs, currrent_page=1, last_page=last_page
    )


@app.route("/p/<page>")
# ‘/’ URL is bound with hello_world() function.
def blog_page(page):
    page = int(page)
    last_page = int(
        list(
            db.paginate(
                db.select(Blog).order_by(desc(Blog.blog_date)),
                page=1,
                per_page=BLOGS_PER_PAGE,
            ).iter_pages()
        )[-1]
    )
    if str(page).isnumeric() and (page > 0 and page < last_page + 1):
        page1 = page
    else:
        page1 = 1
    blogs = db.paginate(
        db.select(Blog).order_by(desc(Blog.blog_date)),
        page=page1,
        per_page=BLOGS_PER_PAGE,
    )
    return render_template(
        "home.html", blogs=blogs, currrent_page=page1, last_page=last_page
    )


@app.route("/b/<blog_slug>", methods=["POST", "GET"])
def blog_slug(blog_slug):
    comment_limit = request.args.get('c', default = 10, type = int)
    if request.method=="POST": 
        if "user_id" in session:
            userid = session["user_id"]
            comment = request.form["blog_comment"]
            if comment != "":
                blog = get_blog_by_slug(blog_slug=blog_slug)
                if blog is not None:
                    temporary_comment = add_comment_by_userid(userid=userid,blog_id=blog.blog_id,blog_comment=comment)
                    if temporary_comment is None:
                        return redirect(url_for("logout"))
                    else:
                        return redirect(request.url)
                else:
                    return "such blog does not exist!"
        else:
            flash("you need to login first!")
            return redirect(url_for("login"))
    else:
        blog = get_blog_by_slug(blog_slug=blog_slug)
        comments = Comment.query.filter_by(blog_id=blog.blog_id).order_by(desc(Comment.comment_date)).limit(comment_limit)
        return render_template("blogpage.html", blog=blog, comments=comments)


@app.route("/login", methods=["POST", "GET"])
def login():
    global userLogin
    if request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passd"]
        print(email, passwd)
        user_with_mail = User.query.filter_by(email=email).first()
        if user_with_mail != None:
            # print("user found")
            # print(user_with_mail.password)
            if user_with_mail.password == passwd:
                # correct password
                # print("logged in!")
                userLogin = True
                session.permanent = True
                session["user_id"] = user_with_mail.id
                flash("you have been logged in!")
                return redirect(url_for("user"))
            else:
                # wrong password
                flash("Wrong password! check again")
                return redirect(url_for("login"))
        # print("user not found")
        flash("This email is not registered!")
        return redirect(url_for("login"))

    else:
        if "user_id" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        passwd = request.form["passd"]
        print(fullname, username, email, passwd)
        is_user_unique = False
        is_email_unique = False
        user_with_mail = User.query.filter_by(email=email).first()
        if user_with_mail == None:
            # username is unique
            is_user_unique = True

        user_with_mail = User.query.filter_by(username=username).first()
        if user_with_mail == None:
            is_email_unique = True

        if is_email_unique and is_user_unique:
            add_user(username=username, fullname=fullname, email=email, password=passwd)
            flash(
                "your email id has been registered! kindly login with the filled details"
            )
            return redirect(url_for("login"))

        else:
            if is_email_unique == False:
                flash("email is already used!")
            if is_user_unique == False:
                flash("username is already used!")
            return redirect(url_for("register"))

    else:
        if "user_id" in session:
            return redirect(url_for("user"))
        else:
            return render_template("register.html")


@app.route("/logout")
def logout():
    global userLogin
    if "user_id" in session:
        flash(f"You have been logged out!", category="info")
    # print("logged out!")
    userLogin = False
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/user")
def user():
    global userLogin
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        if user != None:
            # print("logged in!")
            userLogin = True
            flash(f"Welcome back! {user.fullname}")
            return render_template("user.html")
        else:
            # logout the user
            return redirect(url_for("logout"))
    else:
        flash(f"You have to login first!")
        return redirect(url_for("login"))


@app.route("/editor", methods=["POST", "GET"])
def editor():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        # check if user is blog publisher or not
        if user.is_blog_publisher:
            # if user is blog publisher check if he made GET or POST request
            if request.method == "POST":
                # print("POST happened!")
                blog_title = request.form["blog_title"]
                blog_content = request.form["blog_content"]
                if blog_title != "" and blog_content != "":
                    # print("adding blog!")
                    add_blog(
                        username=user.username,
                        blog_title=blog_title,
                        blog_content=blog_content,
                    )
                    flash("Blog has been succesfully added!")
                    return redirect(url_for("editor"))
                else:
                    # print("not adding blog!")
                    flash("Fields cannot not be empty!")
                    return redirect(url_for("editor"))
            else:
                return render_template("editor.html", user=user)
        else:
            flash(f"You are not an blog publisher!")
            return redirect(url_for("login"))
    else:
        flash(f"You have to login first!")
        return redirect(url_for("login"))


# [ ERROR HANDLING ]
# handles invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html")


if __name__ == "__main__":
    app.run(debug=True)
