from objects.globals import app
from flask import render_template, request, flash, redirect, url_for

from db_models.AdminAuth import AdminAuth

@app.route("/login", methods=['GET','POST'])
async def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login == "" and password == "":
            flash("Вы забыли ввести логин и пароль!")
            return redirect(url_for("login"))

        elif login == "" or password == "":
            flash("Вы забыли ввести логин или пароль!")
            return redirect(url_for("login"))

        else:
            get_password_from_db = await AdminAuth.objects.filter(login=login).all()
            if len(get_password_from_db) > 0:
                get_password_from_db = get_password_from_db[0]
                
                if get_password_from_db.password == password:
                    return redirect(url_for("index"))
                else:
                    flash("Неверный пароль!")
                    return redirect(url_for("login"))
            else:
                flash("Неверный логин!")
                return redirect(url_for("login"))

    return render_template("login.html")