from flask import Blueprint
from project.owners.models import Owner

owners_blueprint = Blueprint('owners', __name__, template_folder = 'templates')