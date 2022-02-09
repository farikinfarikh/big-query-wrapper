from flask import Flask
from flask.json import jsonify
import os
from src.bigquery import bq
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger
from src.config.swagger import template, swagger_config

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"))

        SWAGGER={
            'title': 'BigQuery Wrapper API',
            'uiversion': 3
        }
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(bq)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not founf'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), \
            HTTP_500_INTERNAL_SERVER_ERROR
    
    return app
