from objects.globals import app, ip_adress, admin_password
from flask import render_template, request

from db_models.Applications import Application

@app.route("/applications")
async def applications():

    if request.cookies.get("username") != admin_password:
        return '<a href="/login">Go to login</a>'

    applications_data = await Application.objects.all()

    return render_template("applications.html", applications=applications_data, ip_adress=ip_adress)