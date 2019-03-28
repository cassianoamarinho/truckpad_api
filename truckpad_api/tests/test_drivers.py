import uuid
from datetime import datetime, timedelta

import pytest

from truckpad_api import app
from truckpad_api.app import db
from truckpad_api.models import Driver


@pytest.fixture
def client():
    test_client = app.app.test_client()
    yield test_client


def test_get_period(client):
    driver_id = str(uuid.uuid4())

    db.session.add(Driver(id=driver_id, name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime.now(),
                          has_truck=True, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_get = client.get('api/drivers/period')

    print(resp_get.json)

    assert resp_get.status_code == 200
    assert resp_get.json["qtd_day"] == 1
    assert resp_get.json["qtd_week"] == 1
    assert resp_get.json["qtd_month"] == 1


def test_get_locations(client):
    driver_id = str(uuid.uuid4())

    driver = db.session.merge(Driver(id=driver_id, name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                                     created_date=datetime(1992, 6, 19, 12, 0, 0),
                                     has_truck=True, is_loaded=False, cnh_type="D", truck_type=4,
                                     lat_origin="-23.5506507", lng_origin="-46.6333824",
                                     lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_get = client.get('api/drivers/truck_types/list')

    assert resp_get.status_code == 200
    assert len(resp_get.json[0]["drivers_info"]) == 0
    assert len(resp_get.json[1]["drivers_info"]) == 0
    assert len(resp_get.json[2]["drivers_info"]) == 0
    assert resp_get.json[3]["drivers_info"][0]['truck_type'] == 4
    assert resp_get.json[3]["drivers_info"][0]['lat_destination'] == "-22.9110137"
    assert resp_get.json[3]["drivers_info"][0]['is_loaded'] == False
    assert resp_get.json[3]["drivers_info"][0]['cnh_type'] == "D"
    assert resp_get.json[3]["drivers_info"][0]['created_date'] == driver.created_date.strftime(
        '%Y-%m-%dT%H:%M:%S+00:00')
    assert resp_get.json[3]["drivers_info"][0]['name'] == "Motorista"
    assert resp_get.json[3]["drivers_info"][0]['lng_origin'] == "-46.6333824"
    assert resp_get.json[3]["drivers_info"][0]['born_date'] == driver.born_date.strftime('%Y-%m-%dT%H:%M:%S')
    assert resp_get.json[3]["drivers_info"][0]['lat_origin'] == "-23.5506507"
    assert resp_get.json[3]["drivers_info"][0]['id'] == driver_id
    assert resp_get.json[3]["drivers_info"][0]['gender'] == 2
    assert resp_get.json[3]["drivers_info"][0]['lng_destination'] == "-43.2093727"
    assert resp_get.json[3]["drivers_info"][0]['has_truck'] == True
    assert len(resp_get.json[4]["drivers_info"]) == 0


def test_save_driver(client):
    driver_id = str(uuid.uuid4())

    resp_post = client.post('/api/drivers',
                            headers={'content-type': 'application/json'},
                            json={
                                "id": driver_id,
                                "name": "Motorista",
                                "born_date": "1992-06-29",
                                "gender": 2,
                                "has_truck": False,
                                "is_loaded": True,
                                "cnh_type": "D",
                                "truck_type": 4,
                                "origin_city": "São Paulo",
                                "origin_state": "SP",
                                "destination_city": "Rio de Janeiro",
                                "destination_state": "RJ"
                            })

    resp_get = client.get('/api/drivers/{}'.format(driver_id))

    assert resp_post.status_code == 200
    assert resp_post.json['truck_type'] == resp_get.json['truck_type']
    assert resp_post.json['lat_destination'] == resp_get.json['lat_destination']
    assert resp_post.json['is_loaded'] == resp_get.json['is_loaded']
    assert resp_post.json['cnh_type'] == resp_get.json['cnh_type']
    assert resp_post.json['created_date'] == resp_get.json['created_date']
    assert resp_post.json['name'] == resp_get.json['name']
    assert resp_post.json['lng_origin'] == resp_get.json['lng_origin']
    assert resp_post.json['born_date'] == resp_get.json['born_date']
    assert resp_post.json['lat_origin'] == resp_get.json['lat_origin']
    assert resp_post.json['id'] == resp_get.json['id']
    assert resp_post.json['gender'] == resp_get.json['gender']
    assert resp_post.json['lng_destination'] == resp_get.json['lng_destination']
    assert resp_post.json['has_truck'] == resp_get.json['has_truck']


def test_update_driver(client):
    driver_id = str(uuid.uuid4())

    db.session.add(Driver(id=driver_id, name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime(1992, 6, 19, 12, 0, 0),
                          has_truck=False, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_put = client.put('/api/drivers/{}'.format(driver_id),
                          headers={'content-type': 'application/json'},
                          json={
                              "name": "Motorista Editado",
                              "born_date": "1992-06-29",
                              "gender": 2,
                              "has_truck": True,
                              "is_loaded": True,
                              "cnh_type": "D",
                              "truck_type": 4,
                              "origin_city": "São Paulo",
                              "origin_state": "SP",
                              "destination_city": "Rio de Janeiro",
                              "destination_state": "RJ"
                          })

    resp_get = client.get('/api/drivers/{}'.format(driver_id))

    assert resp_put.status_code == 200
    assert resp_put.json['truck_type'] == resp_get.json['truck_type']
    assert resp_put.json['lat_destination'] == resp_get.json['lat_destination']
    assert resp_put.json['is_loaded'] == resp_get.json['is_loaded']
    assert resp_put.json['cnh_type'] == resp_get.json['cnh_type']
    assert resp_put.json['created_date'] == resp_get.json['created_date']
    assert resp_put.json['name'] == resp_get.json['name']
    assert resp_put.json['lng_origin'] == resp_get.json['lng_origin']
    assert resp_put.json['born_date'] == resp_get.json['born_date']
    assert resp_put.json['lat_origin'] == resp_get.json['lat_origin']
    assert resp_put.json['id'] == resp_get.json['id']
    assert resp_put.json['gender'] == resp_get.json['gender']
    assert resp_put.json['lng_destination'] == resp_get.json['lng_destination']
    assert resp_put.json['has_truck'] == resp_get.json['has_truck']


def test_delete_driver(client):
    driver_id = str(uuid.uuid4())

    db.session.add(Driver(id=driver_id, name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime(1992, 6, 19, 12, 0, 0),
                          has_truck=False, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_delete = client.delete('/api/drivers/{}'.format(driver_id))

    assert resp_delete.status_code == 204

    resp_get = client.get('/api/drivers/{}'.format(driver_id))

    assert resp_get.json['is_removed'] == True


def test_get_count_drivers_has_truck(client):
    db.session.add(Driver(id=str(uuid.uuid4()), name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime(1992, 6, 19, 12, 0, 0),
                          has_truck=True, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    db.session.add(Driver(id=str(uuid.uuid4()), name="Motorista 2", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime(1992, 6, 19, 12, 0, 0),
                          has_truck=True, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_get = client.get('/api/drivers/has_truck/count')

    assert resp_get.status_code == 200
    assert resp_get.json['count_drivers_has_truck'] == 2


def test_get_drivers_is_loaded(client):
    db.session.add(Driver(name="Motorista", born_date=datetime(1992, 6, 19), gender=2,
                          created_date=datetime(1992, 6, 19, 12, 0, 0),
                          has_truck=True, is_loaded=True, cnh_type="D", truck_type=4,
                          lat_origin="-23.5506507", lng_origin="-46.6333824",
                          lat_destination="-22.9110137", lng_destination="-43.2093727"))

    driver_2 = db.session.merge(
        Driver(name="Motorista 2", born_date=datetime(1992, 6, 19), gender=2,
               created_date=datetime(1992, 6, 19, 12, 0, 0),
               has_truck=True, is_loaded=False, cnh_type="D", truck_type=4,
               lat_origin="-23.5506507", lng_origin="-46.6333824",
               lat_destination="-22.9110137", lng_destination="-43.2093727"))

    resp_get = client.get('api/drivers/is_loaded/false')

    print(driver_2)

    assert resp_get.status_code == 200
    assert resp_get.json[0]['truck_type'] == 4
    assert resp_get.json[0]['lat_destination'] == "-22.9110137"
    assert resp_get.json[0]['is_loaded'] == False
    assert resp_get.json[0]['cnh_type'] == "D"
    assert resp_get.json[0]['created_date'] == driver_2.created_date.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    assert resp_get.json[0]['name'] == "Motorista 2"
    assert resp_get.json[0]['lng_origin'] == "-46.6333824"
    assert resp_get.json[0]['born_date'] == driver_2.born_date.strftime('%Y-%m-%dT%H:%M:%S')
    assert resp_get.json[0]['lat_origin'] == "-23.5506507"
    assert resp_get.json[0]['id'] == driver_2.id
    assert resp_get.json[0]['gender'] == 2
    assert resp_get.json[0]['lng_destination'] == "-43.2093727"
    assert resp_get.json[0]['has_truck'] == True
