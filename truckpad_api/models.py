import uuid

from truckpad_api.app import db


def generate_uuid():
    return str(uuid.uuid4())


class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.String(40), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    born_date = db.Column(db.Date(), nullable=False)
    gender = db.Column(db.Integer(), nullable=False)
    has_truck = db.Column(db.Boolean(), default=False, nullable=False)
    is_loaded = db.Column(db.Boolean(), default=False, nullable=False)
    created_date = db.Column(db.DateTime(), default=False, nullable=False)
    cnh_type = db.Column(db.String(5), nullable=False)
    truck_type = db.Column(db.Integer(), nullable=False)
    lat_origin = db.Column(db.String(15), nullable=False)
    lng_origin = db.Column(db.String(15), nullable=False)
    lat_destination = db.Column(db.String(15), nullable=False)
    lng_destination = db.Column(db.String(15), nullable=False)
    is_removed = db.Column(db.Boolean(), default=False, nullable=False)

    def __repr__(self):
        return '<Driver: {} - {}>'.format(self.id, self.name)
