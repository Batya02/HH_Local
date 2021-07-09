from objects.globals import app, ip_adress
from flask import render_template, request

from db_models.Resume import Resume
from db_models.AdminAuth import AdminAuth

@app.route("/resume")
async def resume():
    
    admin_data = await AdminAuth.objects.all()
    admin_data = admin_data[0]

    if request.cookies.get("username") != admin_data.password:
        return 'Do not login'

    resume_data = await Resume.objects.all()

    return render_template("resume.html", resume=resume_data, ip_adress=ip_adress)