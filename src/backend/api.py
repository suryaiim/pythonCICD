from flask import Blueprint
from flask_restplus import Api

from .wallet import ns_wallet

api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    title='API',
)

api.add_namespace(ns_wallet)
