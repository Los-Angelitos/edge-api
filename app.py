from flask import Flask
from flasgger import Swagger, swag_from

from iam.infrastructure.routes import iam as iam_routes
from inventory.infrastructure.population import populate_rfid_cards
from operations_and_monitoring.infrastructure.population import populate_thermostats
from operations_and_monitoring.interfaces.services import monitoring_api as monitoring_routes
from inventory.interfaces.services import inventory_api as inventory_routes
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(iam_routes, url_prefix='/api/v1/iam', name='iam')
app.register_blueprint(monitoring_routes, url_prefix='/api/v1/monitoring', name='monitoring')
app.register_blueprint(inventory_routes, url_prefix='/api/v1/inventory', name='inventory')

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

populate_rfid_cards()
populate_thermostats()


init_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)