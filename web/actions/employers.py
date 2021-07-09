from objects.globals import app, ip_adress
from flask import render_template, request

from db_models.Employers import Employer
from db_models.Applications import Application
from db_models.Users import User
from db_models.AdminAuth import AdminAuth

@app.route("/employers", methods=["GET", "POST"])
async def employers():

    admin_data = await AdminAuth.objects.all()
    admin_data = admin_data[0]

    if request.cookies.get("username") != admin_data.password:
        return 'Do not login'

    main_user:int = 0
    
    if request.method == "POST":

        if "more-information-employer" in request.form:

            main_user = int(request.form.get("more-information-employer"))
        
        elif "one-add-verification-employer" in request.form:
            user_id_ver = main_user = int(request.form.get("one-add-verification-employer"))
            user_ver_status = await User.objects.get(user_id=user_id_ver)
            await user_ver_status.update(verification=1)
        
        elif "one-add-unverification-employer" in request.form:
            user_id_unver = main_user = int(request.form.get("one-add-unverification-employer"))
            user_ver_status = await User.objects.get(user_id=user_id_unver)
            await user_ver_status.update(verification=0)
        
        elif "one-add-in-spam-employer" in request.form:
            user_id_spam = main_user = int(request.form.get("one-add-in-spam-employer"))
            user_spam_status = await User.objects.get(user_id=user_id_spam)
            await user_spam_status.update(spam=1)
        
        elif "one-add-of-unspam-employer" in request.form:
            user_id_unspam = main_user = int(request.form.get("one-add-of-unspam-employer"))
            user_spam_status = await User.objects.get(user_id=user_id_unspam)
            await user_spam_status.update(spam=0)
        
        more_info_employer = await User.objects.filter(user_id=main_user).all()
        applications_data = await Application.objects.filter(user_id=main_user).all()

        return render_template("more-information-employer.html", user_data=more_info_employer, applications=applications_data)

    employers_data = await Employer.objects.all()

    return render_template("employers.html", employers=employers_data, ip_adress=ip_adress)