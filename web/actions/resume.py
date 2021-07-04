from objects.globals import app
from flask import render_template

from db_models.Resume import Resume

@app.route("/resume")
async def resume():
    resume_data = await Resume.objects.all()

    return render_template("resume.html", resume=resume_data)