from flask import Flask, redirect, send_from_directory
from config import app_config
import os

APPLICATION_ROOT = os.getenv("MOUNTPOINT", None)

app = Flask( "redirect", static_folder = None)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return redirect( APPLICATION_ROOT )

