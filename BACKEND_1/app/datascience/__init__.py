# app/datascience/__init__.py

from flask import Blueprint

def create_datascience_blueprint():
    """Create and return the Data Science blueprint.
    All routes are defined in the 'routes' module.
    """
    ds_bp = Blueprint('datascience', __name__)
    # Import routes to register endpoints
    from . import routes  # noqa: F401
    return ds_bp
