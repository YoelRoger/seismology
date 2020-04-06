from flask_restful import Resource
from flask import request


VERIFIED_SEISMS = {
    1: {"id": "1", "datetime": "06/12/2019", "magnitude":"3.5"},
    2: {"id": "2", "datetime": "12/01/2020", "magnitude":"6.3"},
    3: {"id": "3", "datetime": "07/04/2020", "magnitude":"8.2"}
}
UNVERIFIED_SEISMS = {
    1: {"id": "4", "datetime": "04/11/2019", "magnitude":"5.5"},
    2: {"id": "5", "datetime": "22/11/2020", "magnitude":"5.3"},
    3: {"id": "6", "datetime": "03/10/2020", "magnitude":"2.2"}
}
UNVERIFIED_SEISM = {
    1: {"id": "7", "datetime": "16/12/2019", "magnitude":"1.3"},
    2: {"id": "8", "datetime": "14/01/2020", "magnitude":"1.2"},
    3: {"id": "9", "datetime": "17/04/2020", "magnitude":"4.3"}
}
VERIFIED_SEISM = {
    1: {"id": "11", "datetime": "16/12/2019", "magnitude":"1.3"},
    2: {"id": "12", "datetime": "15/01/2020", "magnitude":"1.1"},
    3: {"id": "13", "datetime": "08/04/2020", "magnitude":"6.2"}
}


# Recurso dato sismo
class VerifiedSeism(Resource):
    # Obtener recurso
    def get(self, id):
        if int(id) in VERIFIED_SEISMS:
            return VERIFIED_SEISMS[int(id)]
        return 'NOT FOUND', 404


# Recurso dato sismoS
class VerifiedSeisms(Resource):
    # Obtener recurso

    def get(self):
        return VERIFIED_SEISMS


# Recurso Usismo
class UnverifiedSeism(Resource):
    # Obtener recurso
    def get(self, id):
        if int(id) in UNVERIFIED_SEISM:
            return UNVERIFIED_SEISM[int(id)]
        return 'NOT FOUND', 404

    # Eliminar recurso
    def delete(self, id):
        if int(id) in UNVERIFIED_SEISM:
            del UNVERIFIED_SEISM[int(id)]
            return 'DELETE COMPLETE', 204
        return 'NOT FOUND', 404

    # Modificar recurso
    def put(self, id):
        if int(id) in UNVERIFIED_SEISM:
            unvSeism = UNVERIFIED_SEISM[int(id)]
            data = request.get_json()
            unvSeism.update(data)
            return unvSeism, 201
        return 'NOT FOUND', 404


# Recurso UsismoS
class UnverifiedSeisms(Resource):
    # Obtener recurso
    def get(self):
        return UNVERIFIED_SEISMS
