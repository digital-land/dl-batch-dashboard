from application.controllers.logs import get_log_statuses

from flask import (
    abort,
    current_app,
    Blueprint,
    render_template,
)

frontend = Blueprint("frontend", __name__, template_folder="templates")

@frontend.route('/home')
@frontend.route("/")
def logs_page():
    logs = get_log_statuses()
    return render_template('runs.html', logs=logs)