import json
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from model import ClientData
import tasks


def upload(request):
    # decode json body
    json_data = json.loads(json.dumps(request.json_body))
    ClientData.create_from_json(json_data)
    tasks.mul.delay()  # tells TaskQueue to calculate the results for the added rows
    return Response("OK")


def getresult(request):
    req_id = request.matchdict['id']  # the required id from the request
    foundrow = ClientData.get_result(req_id)
    return Response('{"result":' + str(foundrow.result) + '}')  # returns the result of the row with the required id


config = Configurator()
config.add_route('upload', '/upload')  # upload data to DB and send to task queue
config.add_route('getresult', '/results/{id}')  # get the result for id from the DB
config.add_view(upload, route_name='upload', request_method='POST', renderer='string')
config.add_view(getresult, route_name='getresult', request_method='GET')
app = config.make_wsgi_app()


if __name__ == '__main__':
    server = make_server('0.0.0.0', 4555, app)
    server.serve_forever()
