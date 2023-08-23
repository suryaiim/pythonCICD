from flask import Flask, redirect, request, url_for
from flask.logging import default_handler
from wallet import Wallet
import random
import logging
from logger import setup_logging

from config import app_config

from backend.api import api_bp

# Set up Flask server and extensions
def create_app():
    server = Flask(__name__)

    ''' Setup the common attributes in here '''
    server.config.from_object( app_config )

    # Setup logging
    setup_logging(server)

    server.register_blueprint(api_bp)

    @server.route('/status')
    def status():
        return "{} running".format(app_config.APP_NAME)

    @server.route('/')
    def redirectall():
        return redirect(url_for('status'), code=302)

    return server


if __name__ == '__main__':
    server = create_app()
    server.run(
            host='0.0.0.0',
            port=app_config.APP_PORT,
            use_reloader=False,
    )
