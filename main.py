# Mjolnir
from src.controllers.controller import app
from src.infrastructures.sqlite.infrastructure import SqliteInfrastructure

# Third party
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)

SqliteInfrastructure.script_create_client_table()
SqliteInfrastructure.script_create_car_table()

app.run()
