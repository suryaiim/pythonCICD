import gevent.monkey
gevent.monkey.patch_all()

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from config import app_config
from base import app as redirecter
from app import create_app

app  = create_app()
#We want X-Real-IP to come through for logging
#app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

app = DispatcherMiddleware(redirecter,{
    app_config.MOUNTPOINT:     app
    })

