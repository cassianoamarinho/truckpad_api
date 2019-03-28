import datetime
import json

from flask import Blueprint, Response, request
from marshmallow import fields, Schema
from truckpad_api.app import db
from truckpad_api.app import app
from truckpad_api.models import Driver
from truckpad_api.utils import get_geolocation

drivers_bp = Blueprint('drivers', __name__)


class SetDriverSchema(Schema):
    id = fields.String(required=False)
    name = fields.String(required=True)
    born_date = fields.Date(required=True)
    created_date = fields.DateTime(required=False)
    gender = fields.Integer(required=True)
    has_truck = fields.Boolean(required=True)
    is_loaded = fields.Boolean(required=True)
    cnh_type = fields.String(required=True)
    truck_type = fields.Integer(required=True)

    origin_city = fields.String(required=True)
    origin_state = fields.String(required=True)
    destination_city = fields.String(required=True)
    destination_state = fields.String(required=True)

    lat_origin = fields.String(required=False)
    lng_origin = fields.String(required=False)
    lat_destination = fields.String(required=False)
    lng_destination = fields.String(required=False)
    is_removed = fields.Boolean(required=False)

    class Meta:
        strict = True


set_driver_schema = SetDriverSchema()


@drivers_bp.route('/drivers', methods=['POST'])
def create_driver(**kwargs):
    body = set_driver_schema.load(request.json).data

    origin_latitude, origin_longitude = get_geolocation(body['origin_city'], body['origin_state'])
    destination_latitude, destination_longitude = get_geolocation(body['destination_city'], body['destination_state'])

    driver = db.session.merge(
        Driver(id=body['id'], name=body['name'], born_date=body['born_date'], gender=body['gender'],
               has_truck=body['has_truck'], is_loaded=body['is_loaded'], created_date=datetime.datetime.now(),
               cnh_type=body['cnh_type'], truck_type=body['truck_type'],
               lat_origin=origin_latitude, lng_origin=origin_longitude,
               lat_destination=destination_latitude, lng_destination=destination_longitude))

    db.session.commit()

    return Response(json.dumps(set_driver_schema.dump(driver).data), status=200, content_type="application/json")


@drivers_bp.route('/drivers/<driver_id>', methods=['PUT'])
def update_driver(driver_id):
    body = set_driver_schema.load(request.json).data

    origin_latitude, origin_longitude = get_geolocation(body['origin_city'], body['origin_state'])
    destination_latitude, destination_longitude = get_geolocation(body['destination_city'], body['destination_state'])

    driver = db.session.merge(
        Driver(id=driver_id, name=body['name'], born_date=body['born_date'], gender=body['gender'],
               has_truck=body['has_truck'], is_loaded=body['is_loaded'], created_date=datetime.datetime.now(),
               cnh_type=body['cnh_type'], truck_type=body['truck_type'],
               lat_origin=origin_latitude, lng_origin=origin_longitude,
               lat_destination=destination_latitude, lng_destination=destination_longitude))

    db.session.commit()

    return Response(json.dumps(set_driver_schema.dump(driver).data), status=200, content_type="application/json")


@drivers_bp.route('/drivers/<driver_id>', methods=['DELETE'])
def delete_drivers(driver_id):
    db.session.query(Driver).filter_by(id=driver_id).update(dict(is_removed=True))

    db.session.commit()

    return Response(status=204, content_type="application/json")


@drivers_bp.route('/drivers/<driver_id>', methods=['GET'])
def get_drivers_by_id(driver_id):
    driver = db.session.query(Driver).filter(Driver.id == driver_id).first()

    return Response(json.dumps(set_driver_schema.dump(driver).data), status=200,
                    content_type="application/json")


@drivers_bp.route('/drivers/has_truck/count', methods=['GET'])
def get_count_drivers_has_truck():
    drivers = db.session.query(Driver).filter(Driver.has_truck == True).count()

    return Response(json.dumps({"count_drivers_has_truck": drivers}), status=200,
                    content_type="application/json")


@drivers_bp.route('/drivers/is_loaded/false', methods=['GET'])
def get_drivers_is_loaded():
    drivers = db.session.query(Driver).filter(Driver.is_loaded == False).all()

    return Response(json.dumps([set_driver_schema.dump(driver).data for driver in drivers]), status=200,
                    content_type="application/json")


@drivers_bp.route('/drivers/truck_types/list', methods=['GET'])
def get_locations():
    json_return = [{"code": truck['code'],
                    "description": truck['description'],
                    "drivers_info": [set_driver_schema.dump(driver).data for driver in
                                     db.session.query(Driver).filter(Driver.truck_type == truck['code']).all()]
                    } for truck in app.config['TRUCK_TYPES']]

    return Response(json.dumps(json_return), status=200, content_type="application/json")


@drivers_bp.route('/drivers/period', methods=['GET'])
def get_period_drivers_is_loaded():
    period_return = {
        "qtd_day": db.session.query(Driver).filter(Driver.is_loaded == True).filter(
            Driver.created_date >= datetime.datetime.now() - datetime.timedelta(days=1)).count(),

        "qtd_week": db.session.query(Driver).filter(Driver.is_loaded == True).filter(
            Driver.created_date >= datetime.datetime.now() - datetime.timedelta(days=7)).count(),

        "qtd_month": db.session.query(Driver).filter(Driver.is_loaded == True).filter(
            Driver.created_date >= datetime.datetime.now() - datetime.timedelta(days=30)).count()
    }

    return Response(json.dumps(period_return), status=200, content_type="application/json")
