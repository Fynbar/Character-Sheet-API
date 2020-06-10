import json
from flask import Flask
# , request
from flask_restful import Resource, Api
from flask_cors import CORS
# , Api
from flask.views import MethodView
# , cross_origin
# from flask.json import jsonify
# from flask.views import View, MethodView
# from pprint import pprint
from thermo_state.thermo_state import StateAPI, StateLimitAPI
# from beam_bending.beam_bending import BeamAPI, BeamEndCondAPI
# , ThermoState


class BaseAPI(MethodView):
    def get(self):
        # print(state_id)
        return json.dumps({'text': 'Hello World!'})

    def post(self):
        # create a new state
        pass

    def delete(self):
        # delete a single state
        pass

    def put(self, state_id):
        # update a single state
        pass

# with open('./Saved Files/srd_5e_monsters.json') as f:
#     monsters = json.load(f)

# monster_list = []

# for i, m in enumerate(monsters):
#     m['id'] = i + 1
#     monster_list.append(SetProperties(m))

# with open('Saved Files/monster.json', 'w') as json_file:
#     json.dump(monster_list, json_file)


app = Flask(__name__)
CORS(app)
app.app_context()
api = Api(app)
# 
# 
# @app.route("/")
# def hello():
#     return json.dumps({'text': 'Hello World!'})


base_view = BaseAPI.as_view('base_api')

app.add_url_rule('/', view_func=base_view,
                 methods=['GET', 'PUT', 'DELETE'])


class Employees(Resource):
    def get(self):
        return {'employees': [{'id': 1, 'name': 'Balram'},
                              {'id': 2, 'name': 'Tom'}]}


api.add_resource(Employees, '/employees')  # Route_1

# Thermodynamic States
state_view = StateAPI.as_view('state_api')
app.add_url_rule('/states/', defaults={'state_id': None},
                 view_func=state_view, methods=['GET', ])
app.add_url_rule('/states/', view_func=state_view, methods=['POST', ])
app.add_url_rule('/states/<int:state_id>', view_func=state_view,
                 methods=['GET', 'PUT', 'DELETE'])
# Api to get the max and min saturation temp
limit_view = StateLimitAPI.as_view('limit_api')
app.add_url_rule('/stateLimits/', defaults={'material': None},
                 view_func=limit_view, methods=['GET', ])

# # Beam Bending
# bending_view = BeamAPI.as_view('bending_api')

# app.add_url_rule('/bendings/', view_func=bending_view, methods=['POST', ])
# app.add_url_rule('/bendings/<int:bending_id>', view_func=bending_view,
#                  methods=['GET', 'PUT', 'DELETE'])
# # Api to get the types of end conditions
# endCond_view = BeamEndCondAPI.as_view('endCond_api')

# app.add_url_rule('/beamEnds/', view_func=endCond_view, methods=['GET', ])

# # api.add_resource(ThermoState, '/allstates') # Route_2

if __name__ == '__main__':
    print('Loading Backend...')
    app.run(port=5002)
