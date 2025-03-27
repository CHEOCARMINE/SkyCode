from flask import Blueprint, render_template

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports")
def show_reports():
    return "Página de reportes en construcción 🚧"
