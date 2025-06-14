﻿from flask import Flask
from flasgger import Swagger, swag_from

from iam.infrastructure.routes import iam as iam_routes
from operations_and_monitoring.interfaces.services import monitoring_api as monitoring_routes
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(iam_routes, url_prefix='/api/v1/iam', name='iam')
app.register_blueprint(monitoring_routes, url_prefix='/api/v1/monitoring', name='monitoring')

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "SweetManager IoT Edge API",
        "description": "API Restful for managing IoT devices in the SweetManager system.",
        "version": "1.0.0",
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }}
)

init_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)