# from flask.json import jsonify
from flask_restful import Resource
# , Api
from flask.views import MethodView
import json


class ThermoState(Resource):
    def __init__(self, T, P, s_f, h_f, u_f, v_f, s_g, h_g, u_g, v_g):
        self.Temperature = T
        self.Pressure = P
        self.Entropy = [s_f, s_g]
        self.Enthalpy = [h_f, h_g]
        self.InternalEnergy = [u_f, u_g]
        self.SpecificDensity = [v_f, v_g]

    def toJson(self):
        return json.dumps(self.toJsonFormat())

    def toJsonFormat(self):
        return {'Temperature': self.Temperature,
                'Pressure': self.Pressure,
                'Entropy': self.Entropy,
                'Enthalpy': self.Enthalpy,
                'InternalEnergy': self.InternalEnergy,
                'SpecificDensity': self.SpecificDensity
                }


class StateAPI(MethodView):
    def get(self, state_id):
        print(state_id)
        return ThermoState(100, 101.42, 1.3072, 419.17, 419.06, 0.001043,
                           7.3542, 2675.6, 2506.0, 1.6720).toJson()

    def post(self):
        # create a new state
        pass

    def delete(self, state_id):
        # delete a single state
        pass

    def put(self, state_id):
        # update a single state
        pass


class StateLimitAPI(MethodView):
    def get(self, material):
        return json.dumps([ThermoState(0.01, 0.617, 0, 0.001, 0, 0.001, 9.1556,
                                       2500.9, 2374.9, 206).toJsonFormat(),
                           ThermoState(373.95, 22064, 4.407, 2084.3, 2015.7,
                                       0.003106, 4.407, 2084.3, 2015.7,
                                       0.003106).toJsonFormat()])
