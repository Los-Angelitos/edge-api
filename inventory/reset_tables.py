# Borra y crea la tabla de nuevo según el modelo
from inventory.infrastructure.models import RFIDCard
from shared.infrastructure.database import db

db.connect()
db.drop_tables([RFIDCard])
db.create_tables([RFIDCard])
db.close()