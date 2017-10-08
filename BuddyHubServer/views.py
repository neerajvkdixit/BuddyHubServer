from django.http import HttpResponse
from django.http import JsonResponse
from pymongo import MongoClient
import urllib.parse
from bson.json_util import dumps
import json
def fetchdata_getcitylist(request):
    response_data = {}
    url = 'mongodb://%s:%s@127.0.0.1/buddyhub' % (urllib.parse.quote_plus("buddyhub"), urllib.parse.quote_plus("leela@491"))
    client = MongoClient(url)
    citycollection = client.buddyhub.city_data
    projection = {"name": True , "url" : True , "_id":False }
    default_city = "Noida"
    response_data['result'] = 'success'
    response_data['data'] = {}
    cursor = citycollection.find({},projection);
    response_data['data']["cities"] = json.loads(dumps(cursor))
    response_data['data']["default"] = default_city 
    return JsonResponse(response_data)

def post_propertydata(request):
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {}
    return JsonResponse(response_data)
