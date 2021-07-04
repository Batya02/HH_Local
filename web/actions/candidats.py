from objects.globals import app
from flask import render_template

from db_models.Candidats import Candidat

@app.route("/candidats")
async def candidats():
    candidats_data = await Candidat.objects.all()

    return render_template("candidats.html", candidats=candidats_data)