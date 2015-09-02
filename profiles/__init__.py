from flask import Blueprint

import os

bp_profiles = Blueprint(
    'bp_profiles', __name__, static_url_path='/static/profiles',
    static_folder=os.path.join('static', 'profiles')
)
