from secrets import token_urlsafe
from application.controllers.logs import get_errored_runs
from concurrent.futures import ThreadPoolExecutor
import application.db as db

from flask import (
    abort,
    current_app,
    Blueprint,
    render_template,
)

frontend = Blueprint("frontend", __name__, template_folder="templates")
executor = ThreadPoolExecutor(5)

@frontend.route('/home')
@frontend.route("/")
def landing_page():
    token = token_urlsafe(32)
    executor.submit(get_and_store_logs, token)
    return render_template('loading.html', token=token)

@frontend.route("/runs/<token>")
def runs(token):
    (token_status, logs) = db.get_token(token)
    if token_status == "completed":
        return render_template("runs.html", logs=logs)
    else:
        abort(404)

@frontend.route("/check_status/<token>")
def check_status(token):
    (token_status,logs) = db.get_token(token)
    return {"status" : token_status if token_status else "not found"}

def get_and_store_logs(token):
    db.add_pending_token(token)
    logs = get_errored_runs()
    db.update_token_to_complete(token, logs)