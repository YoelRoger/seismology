from flask import Blueprint, render_template, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
import json


from ..utilities.functions import sendRequest


sensor = Blueprint("sensor", __name__, url_prefix="/sensor")


@sensor.route("/")
@register_breadcrumb(sensor,".",'Sensors')
def index():
    req = sendRequest(method="get", url="/sensors", auth=True)
    sensors = json.loads(req.text)['Sensors']
    title = "Sensors"
    return render_template("sensors.html",title=title,sensors=sensors)


@sensor.route("/view/<int:id>")
@register_breadcrumb(sensor, '.view', 'View')
def view(id):
    req = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
    if (req.status_code == 404):
        flash("Sensor not found", "danger")
        return redirect(url_for("sensor.index"))
    sensor = json.loads(req.text)
    title = "Sensor View"
    return render_template("sensor-view.html", title=title, sensor=sensor)
