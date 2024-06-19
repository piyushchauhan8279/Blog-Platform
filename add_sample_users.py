from main import app,add_user,delete_user_by_username
if __name__ == "__main__":
    # [ ADD NEW USERS ]
    with app.app_context():
        newuser = add_user("yash_garg","yg292001@mail.com","yash1234","Yash Garg")
        print(newuser)
        newuser = add_user("yash_garg1","yg2920011@mail.com","yash11234","Yash Garg1")
        print(newuser)
    # [ DELETE EXISITING USER]
    # del_user = delete_user_by_username("yash_garg")
    # print(del_user)