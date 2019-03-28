class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///truckpad.db'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TRUCK_TYPES = [{"code": 1, "description": "Caminhão 3/4"},
                   {"code": 2, "description": "Caminhão Toco"},
                   {"code": 3, "description": "Caminhão ​Truck"},
                   {"code": 4, "description": "Carreta Simples"},
                   {"code": 5, "description": "Carreta Eixo Extendido"}]

    GENDER_TYPES = [{"code": 1, "description": "Feminino"},
                    {"code": 2, "description": "Masculino"}]


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///test_truckpad.db'
    DEBUG = True
    TESTING = True
