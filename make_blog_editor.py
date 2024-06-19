from main import app,make_user_blog_publisher_by_email
# creates the sample blogs
if __name__ == "__main__":
    with app.app_context():
        publisher1 = make_user_blog_publisher_by_email("yg292001@mail.com")
        print(publisher1)