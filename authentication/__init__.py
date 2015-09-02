from flask import Blueprint

bp_authentication = Blueprint(
    'bp_authentication', __name__, template_folder='templates'
)

DEFAULT_PAGE = 'bp_profile.profiledetail'
