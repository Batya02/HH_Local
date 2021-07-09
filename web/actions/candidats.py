from objects.globals import app, ip_adress
from flask import render_template, request

from db_models.Candidats import Candidat
from db_models.Users import User
from db_models.AdminAuth import AdminAuth

@app.route("/candidats", methods=["GET", "POST"])
async def candidats():

    admin_data = await AdminAuth.objects.all()
    admin_data = admin_data[0]

    if request.cookies.get("username") != admin_data.password:
        return '<a href="/login">Go to login</a>'

    main_user:int = 0

    if request.method == "POST":
        if "more-information-candidat" in request.form:
            main_user = int(request.form.get("more-information-candidat"))

        elif "one-add-verification-candidat" in request.form:
            user_id_ver = main_user = int(request.form.get("one-add-verification-candidat"))
            user_ver_status = await User.objects.get(user_id=user_id_ver)
            await user_ver_status.update(verification=1)
        
        elif "one-add-unverification-candidat" in request.form:
            user_id_unver = main_user = int(request.form.get("one-add-unverification-candidat"))
            user_ver_status = await User.objects.get(user_id=user_id_unver)
            await user_ver_status.update(verification=0)
        
        elif "one-add-in-spam-candidat" in request.form:
            user_id_spam = main_user = int(request.form.get("one-add-in-spam-candidat"))
            user_spam_status = await User.objects.get(user_id=user_id_spam)
            await user_spam_status.update(spam=1)
        
        elif "one-add-of-unspam-candidat" in request.form:
            user_id_unspam = main_user = int(request.form.get("one-add-of-unspam-candidat"))
            user_spam_status = await User.objects.get(user_id=user_id_unspam)
            await user_spam_status.update(spam=0)
        
        more_info_candidat = await User.objects.filter(user_id=main_user).all()
        return render_template("more-information-candidat.html", user_data=more_info_candidat)

    candidats_data = await Candidat.objects.all()
    return render_template("candidats.html", candidats=candidats_data, ip_adress=ip_adress)