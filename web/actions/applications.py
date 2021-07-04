from objects.globals import app
from flask import render_template

from db_models.Applications import Application

@app.route("/applications")
async def applications():
    applications_data = await Application.objects.all()

    return render_template("applications.html", applications=applications_data)