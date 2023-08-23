import logging
import pprint
import sys
import os
import socket
import pprint
from gunicorn import glogging

from flask import request

class RequestFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        try:
            record.url = request.url
        except:
            record.url = "EMPTY_URL"

        record.hostname = socket.gethostname()
        record.base_hostname = os.getenv("BASE_HOSTNAME", "EMPTYHOST")

        try:
            record.remote_addr = request.remote_addr
        except:
            record.remote_addr = "-"

        return super(RequestFormatter, self).format(record)

def setup_logging(app):

    from flask.logging import default_handler

    #This is imported by gunicorn, it needs to be top level
    request_log_formatter = RequestFormatter(
            '[%(asctime)s] [%(base_hostname)s:%(hostname)s:%(process)3d] [%(levelname)-7s] [%(remote_addr)-15s] %(url)s :: %(pathname)s:%(lineno)d %(message)s'
    )


    default_handler.setFormatter(request_log_formatter)
    if not 'pytest' in sys.modules:
        app.logger.error("Startup test-error message")
        app.logger.info("app.config:\n" + pprint.pformat(app.config))


class CustomLogger(glogging.Logger):
    """Custom logger for Gunicorn log messages."""

    def setup(self, cfg):
        """Configure Gunicorn application logging configuration."""
        super().setup(cfg)

        """
        TODO override the date format to ISOsomething standard...
        """
        #general_fmt = r"%(asctime)s [%(process)3d] [%(levelname)-7s] %(message)s"
        #Gunicorn 'access' somehow has a very different requestion context. So the ip getting is left out, it is inserted by access below
        general_formatter = RequestFormatter(
            '[%(asctime)s] [%(base_hostname)s:%(hostname)s:%(process)3d] [%(levelname)-7s] %(message)s'
        )
        #print(self.cfg.access_log_format)
        #self.cfg.access_log_format = general_fmt

        # Override Gunicorn's `error_log` configuration.
        self._set_handler( self.error_log, cfg.errorlog, general_formatter )

        #Push the general format at our the access formatter, which will publish specialised messages
        self._set_handler( self.access_log, cfg.accesslog, general_formatter )


    def access(self, resp, req, environ, request_time):
        """ See http://httpd.apache.org/docs/2.0/logs.html#combined
        for format details
        """
        #print("Access got; resp: {}, req: {} environ: {}, request_time: {}".format( resp, req, environ, request_time ) )
        #print("access log format is: {}".format( self.cfg.access_log_format ))

        if not (self.cfg.accesslog or self.cfg.logconfig or
           self.cfg.logconfig_dict or
           (self.cfg.syslog and not self.cfg.disable_redirect_access_to_syslog)):
            return

        # wrap atoms:
        # - make sure atoms will be test case insensitively
        # - if atom doesn't exist replace it by '-'
        safe_atoms = self.atoms_wrapper_class(self.atoms(resp, req, environ,
            request_time))

        #original access log format:
        #%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
        """
        %(h)s remote_addr 192.168.176.1
        %(l)s (literally a dash) -
        %(u) getuser or '-' -
        %(t)s now : [04/Jun/2019:16:21:53 +1000]
        %(r)s "request_method, raw_uri, server_protocol" : "POST /underwriting/_dash-update-component HTTP/1.1"
        %(s)s status 204
        %(b)s resp.sent 0
        %(f)s http_referer   "http://localhost:8007/underwriting/fleet/home"
        %(a)s useragent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
        """
        #To match the general fmt: time, [processpid] [levelname] message
        #access_log_format = "%(t)s %(h)s [%(p)s] [INFO] %(r)s %(s)s %(b)s %(f)s %(a)s"
        #Because we're using the general formatter wrapping this:
        #access_log_format = "[%(h)-15s] %(r) %(s)s %(b)s %(f)s %(a)s"
        access_log_format = "[%(h)-15s] %(r)s %(s)s %(b)s %(f)s %(a)s"

        try:
            self.access_log.info( access_log_format, safe_atoms)
        except:
            self.error(traceback.format_exc())

