from objects.globals import app, ip_adress
from flask import render_template, request

from db_models.Applications import Application
from db_models.AdminAuth import AdminAuth

@app.route("/applications")
async def applications():

    admin_data = await AdminAuth.objects.all()
    admin_data = admin_data[0]

    if request.cookies.get("username") != admin_data.password:
        return 'Do not login'

    applications_data = await Application.objects.all()

    return render_template("applications.html", applications=applications_data, ip_adress=ip_adress)