# from flask.json import jsonify
# from flask_restful import Resource
# , Api
from flask.views import MethodView
import json
from flask import request, make_response
from flask.json import jsonify
# from flask_restful import Resource
# , Api
# from flask.views import MethodView


class SaveJSONAPI(MethodView):
    def get(self):
        # print(state_id)
        return json.dumps({'text': 'Hello World!'})

    def post(self):
        print("Post Attempt:",request.is_json)

        if request.is_json:
            req_data = request.get_json()
            filemane = 'Saved Files/{}.json'.format(req_data['name'])
            with open(filemane, 'w') as json_file:
                print(req_data)
                print(req_data['name'])
                print(jsonify(req_data))
                json.dump(req_data['body'], json_file)
            return make_response(jsonify(req_data['body']))
        else:
            return make_response(jsonify({'response': 'Error non-json type'}))

    def delete(self):
        # delete a single state
        pass

    def put(self):
        # update a single state
        pass

    def jsonWrite(name, data):
        # req_data = request.get_json()
        filemane = 'Saved Files/{}.json'.format(name)
        with open(filemane, 'w') as json_file:
            # print(req_data)
            # print(req_data['name'])
            # print(jsonify(req_data))
            json.dump(data, json_file)
    def jsonRead(name):
        # req_data = request.get_json()
        filename = 'Saved Files/{}.json'.format(name)
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data