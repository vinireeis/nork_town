# Mjolnir
from src.controllers.controller import app
from src.infrastructures.sqlite.infrastructure import SqliteInfrastructure

SqliteInfrastructure.script_create_customer_table()
SqliteInfrastructure.script_create_car_table()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
