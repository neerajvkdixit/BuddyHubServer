from django.http import HttpResponse
from django.http import JsonResponse
from pymongo import MongoClient
import urllib.parse
from bson.json_util import dumps
import json
from django.views.decorators.csrf import csrf_exempt
import hashlib
from python_modules.mongohelper import MongoDao
def fetchdata_getcitylist(request):
    response_data = {}
    projection = {"name": True , "url" : True , "_id":False }
    default_city = "Noida"
    response_data['result'] = 'success'
    response_data['data'] = {}
    mongodao = MongoDao("buddyhub")
    res = mongodao.findAll("city_data",{},projection)
    response_data['data']["cities"] = res
    response_data['data']["default"] = default_city 
    return JsonResponse(response_data)
@csrf_exempt
def post_propertydata(request):
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {}
    request_body = request.body
    request_body = request_body.decode("utf-8")
    prop_json = json.loads(request_body)
    if("property" not in prop_json.keys() or prop_json["property"] != 1):
        response_data['result'] = 'error'
        response_data['msg'] = 'input data is not property data'
    prop_key = gethashkeyofprop(prop_json)
    mongodao = MongoDao("buddyhub")
    prop_po = mongodao.findByKey("propertydata","prop_key",prop_key,False)
    if(prop_po is None):
        prop_json["prop_key"] = prop_key
        prop_po = prop_json
    prop_po["screening"] = 0
    res = mongodao.insertpo("propertydata",prop_po)
    response_data["message"] = "property updated with id is =>"+str(res)
    return JsonResponse(response_data)

def gethashkeyofprop(prop_json):
    user_profile_link = ""
    title = ""
    locality = ""
    if("user" in prop_json.keys() and "userProfileUrl" in prop_json["user"]):
        user_profile_link = prop_json["user"]["userProfileUrl"]
    user_profile_link_hash = hashlib.md5(user_profile_link.encode()).hexdigest()[:10]
    if("title" in prop_json.keys()):
        title = prop_json["title"]
    titlehash = hashlib.md5(title.encode()).hexdigest()[:10]
    if("locality" in prop_json.keys()):
        locality = prop_json["locality"]
    localityhash = hashlib.md5(locality.encode()).hexdigest()[:10]
    keyhash = user_profile_link_hash + titlehash + localityhash
    return keyhash
