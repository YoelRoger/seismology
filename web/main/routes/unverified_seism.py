from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from flask_breadcrumbs import register_breadcrumb
from ..utilities.functions import sendRequest
from ..forms.unverified_seism import UnverifiedSeismEdit, UnverifiedSeismsFilter
from flask_login import login_required


unverified_seism = Blueprint("unverified_seism", __name__, url_prefix="/unverified-seism")


@unverified_seism.route("/")
@login_required
@register_breadcrumb(unverified_seism, '.', 'Unverified Seisms')
def index():
    # Armamos el filtro
    filter = UnverifiedSeismsFilter(request.args, meta={"csrf": False})
    req = sendRequest(method="get", url="/sensors-info")
    filter.sensorId.choices = [
        (int(sensor["id"]), sensor["name"]) for sensor in json.loads(req.text)['Sensors']
    ]
    filter.sensorId.choices.insert(0, [0, "All Sensor"])
    data = {}
    # Aplicamos los filtros
    # Validar formulario de filtro
    if filter.validate():
        if filter.sensorId.data != None and filter.sensorId.data != 0:
            data["sensorId"] = filter.sensorId.data
        # Datetime
        if filter.from_datetime.data and filter.to_datetime.data:
            if filter.from_datetime.data == filter.to_datetime.data:
                data["datetime"] = filter.to_datetime.data.strftime('%Y-%m-%d %H:%M')
        if filter.from_datetime.data != None:
            data["from_date"] = filter.from_datetime.data.strftime('%Y-%m-%d %H:%M')
        if filter.to_datetime.data != None:
            data["to_date"] = filter.to_datetime.data.strftime('%Y-%m-%d %H:%M')

    # Ordenamiento
    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    req = sendRequest(method="get", url="/unverified-seisms", data=json.dumps(data), auth=True)

    if req.status_code == 200:

        unverified_seisms = json.loads(req.text)["Unverified-Seisms"]  # Cargamos los sismos verificados
        # Cargamos los datos de paginacion cantidad de paginas pagina y paginas a ver
        pagination = {}
        pagination["total"] = json.loads(req.text)["total"]
        pagination["pages"] = json.loads(req.text)["pages"]
        pagination["current_page"] = json.loads(req.text)["page"]
        title = "Unverified Seisms List"
        return render_template("unverified-seisms.html", title=title, unverified_seisms=unverified_seisms,
                               filter=filter,
                               pagination=pagination, )
    else:
        redirect(url_for("unverified_seism.index"))

@unverified_seism.route("/view/<int:id>")
@login_required
@register_breadcrumb(unverified_seism, '.view', 'View')
def view(id):
    r = requests.get(current_app.config["API_URL"]+"/unverified-seism/"+str(id),headers={"content-type":"application/json"})
    if (r.status_code == 404):
        return redirect(url_for("unverified_seism.index"))
    unverified_seism = json.loads(r.text)
    title = "Unverified Seism View"
    return render_template("unverified_seism.html", title=title, unverified_seism=unverified_seism)


@unverified_seism.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):
    form = UnverifiedSeismEdit()
    if not form.is_submitted():
        req = sendRequest(method="get", url="/unverified-seism/" + str(id), auth=True)
        if (req.status_code == 404):
            flash("Unverified Seism not found","danger")
            return redirect(url_for("unverified_seism.index"))
        unverified_seism = json.loads(req.text)
        form.depth.data = unverified_seism["depth"]
        form.magnitude.data = unverified_seism["magnitude"]
        form.verified.data = unverified_seism["verified"]

    if form.validate_on_submit():
        unverified_seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data,
            "verified": form.verified.data,
        }
        data = json.dumps(unverified_seism)
        req = sendRequest(method="put", url="/unverified-seism/" + str(id), data=data, auth=True)
        flash("Unverified Seism has been edited","success")
        return redirect(url_for("unverified_seism.index"))
    return render_template("edit-unverifiedseism.html", form=form, id=id)


@unverified_seism.route('delete/<int:id>')
#@login_required
def delete(id):
    req = sendRequest(method="delete", url="/unverified-seism/" + str(id), auth=True)
    flash("Unverified Seism has been deleted", "danger")
    return redirect(url_for('unverified_seism.index'))
