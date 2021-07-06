from objects.globals import app
from flask import render_template, request, redirect, url_for, jsonify

from db_models.Users import User

from requests import get
from json import loads

from objects.globals import config

@app.route("/", methods=["GET", "POST"])
async def index():

    user_info = loads(get(config["USER_INFO_URL"]).text)
    ip_adress = user_info["query"]

    if request.method == "POST":
        if "get-user-id" in request.form:
            main_user = request.form.get("get-user-id")
                
            user_data = await User.objects.filter(user_id=main_user).all()
        
            return render_template("find_user.html", user_data=user_data)
        
        elif "one-add-verification-find_user" in request.form:
            user_id_ver = main_user = int(request.form.get("one-add-verification-find_user"))
            user_ver_status = await User.objects.get(user_id=user_id_ver)
            await user_ver_status.update(verification=1)
        
        elif "one-add-unverification-find_user" in request.form:
            user_id_unver = main_user = int(request.form.get("one-add-unverification-find_user"))
            user_ver_status = await User.objects.get(user_id=user_id_unver)
            await user_ver_status.update(verification=0)
        
        elif "one-add-in-spam-find_user" in request.form:
            user_id_spam = main_user = int(request.form.get("one-add-in-spam-find_user"))
            user_spam_status = await User.objects.get(user_id=user_id_spam)
            await user_spam_status.update(spam=1)
        
        elif "one-add-of-unspam-find_user" in request.form:
            user_id_unspam = main_user = int(request.form.get("one-add-of-unspam-find_user"))
            user_spam_status = await User.objects.get(user_id=user_id_unspam)
            await user_spam_status.update(spam=0)
        
        user_find_data= await User.objects.filter(user_id=main_user).all()
        return render_template("find_user.html", user_data=user_find_data)

    return render_template("index.html", ip_adress=ip_adress)