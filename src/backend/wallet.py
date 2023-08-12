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

@ns_wallet.route("/add")
class WalletAddFunds(Resource):
    def post(self):
        json = request.get_json()
        amount = json.get('amount')
        wallet.add_cash(amount)
        return{'balance': wallet.balance}

@ns_wallet.route("/remove")
class WalletRemoveFunds(Resource):
    def post(self):
     json = request.get_json()
     amount = json.get('amount')
     wallet.spend_cash(amount)
     return{'balance': wallet.balance}
