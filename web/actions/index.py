from objects.globals import app
from flask import render_template, request, redirect, url_for

from db_models.Users import User

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        if "get-user-id" in request.form:
            user_id = request.form.get("get-user-id")
                
            user_data = await User.objects.filter(user_id=user_id).all()
        
            return render_template("find_user.html", user_data=user_data)

    return render_template("index.html")

@app.route("/find_user", methods=["GET", "POST"])
async def find_user():
    user_id = request.form.get("get-user-id")
                
    user_data = await User.objects.filter(user_id=user_id).all()
        
    return render_template("find_user.html", user_data=user_data)