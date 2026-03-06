from http import cookies
from flask import (render_template ,
                redirect ,
                url_for ,
                request ,
                Flask,
                session)
from databaser import *


def init_routes(app:Flask):
    @app.route("/")
    def home():
        if session.get("username") :
            print("==>SESSION FOUND")
            if username_exists(session.get("username")) :
                print("==>USER EXISTS")
                return render_template("index.html")
            print("==>USER NOT EXISTS (session cleared)")
            session.clear()
        print("===>NO SESSION")
        return redirect(url_for("login"))
    @app.route("/login",methods=["POST","GET"])
    def login() :
        if session.get("username") :
            # user already loged in and save infos
            print(f"FOUND SAVED LOGIN : \n\t{session['username']}")
            return render_template("login.html")
        else :
            # if post method
            if request.method == "POST" :
                # get infos
                username = request.form.get("username")
                password = request.form.get("password")
                if not username_exists(username) :
                    return render_template("login.html",username_error="user not found")
                else :
                    if not pass_of_user(username) == password :
                        return render_template("login.html",password_error = "password incorrect")
                    else :
                        # save session
                        session["username"] = username
                        # redirect to home
                        return redirect(url_for("home"))
        return render_template("login.html",username_error="",password_error="")
    @app.route("/sign")
    def sign() :
        pass
    @app.route("/clear",methods=["POST"])
    def clear():
        url = request.form.get("url")
        session.clear()
        return redirect(url_for(url))