from application.controllers.logs import get_errored_runs
from flask import (
    current_app,
    Blueprint,
    render_template,
)

frontend = Blueprint("frontend", __name__, template_folder="templates")

@frontend.route("/")
def builds():
    logs = get_errored_runs()
    return render_template("builds.html", logs=logs)
