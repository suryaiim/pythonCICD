"""
Reference this file in the gunicorn cli options.
ie:
    Format: PATH or file:PATH or python:modulename
--config gunicorn_config.py

"""
# TODO set this as the app name from config
proc_name = 'test_api'

#from wsgigunicorn import app as dispatcher_app
#from wsgigunicorn import db
#import os

def post_fork(server, worker):
    """
    Currently here as a placeholder if the dashboard root page ever requires
    some form of forking
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)
    server.log.info("Exec post forking" )
