from objects.globals import app, ip_adress, admin_password
from flask import render_template, request

from db_models.Resume import Resume

@app.route("/resume")
async def resume():
    
    if request.cookies.get("username") != admin_password:
        return '<a href="/login">Go to login</a>'

    resume_data = await Resume.objects.all()

    return render_template("resume.html", resume=resume_data, ip_adress=ip_adress)