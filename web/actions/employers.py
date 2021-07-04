from objects.globals import app
from flask import render_template

from db_models.Employers import Employer

@app.route("/employers")
async def employers():
    employers_data = await Employer.objects.all()

    return render_template("employers.html", employers=employers_data)