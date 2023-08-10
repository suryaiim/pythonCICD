from flask import request
from flask_restplus import Resource, abort, Namespace
from wallet import wallet

ns_wallet = Namespace('wallet', 'Endpoints for managing a wallet balance')

@ns_wallet.route("/")
class Wallet(Resource):
    def post(self):
        # Load and validate request payload.
        json = request.get_json()
        # Return results
        return abort()

    def get(self):
        return "Wallet contains {}".format(wallet)
