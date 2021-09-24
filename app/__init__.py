from flask import Flask

from logging.config import dictConfig

#from werkzeug.middleware.dispatcher import DispatcherMiddleware

#from prometheus_client import make_wsgi_app


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
# app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
#     '/metrics': make_wsgi_app()
# })


from app import routes

