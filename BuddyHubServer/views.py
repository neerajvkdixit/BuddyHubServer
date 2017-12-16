from django.http import HttpResponse
from django.http import JsonResponse
from pymongo import MongoClient
import urllib.parse
from bson.json_util import dumps
import json
from django.views.decorators.csrf import csrf_exempt
import hashlib
from python_modules.mongohelper import MongoDao
from django.conf import settings

def fetchdata_getcitylist(request):
    response_data = {}
    projection = {"name": True , "url" : True , "_id":False }
    default_city = "Noida"
    response_data['result'] = 'success'
    response_data['data'] = {}
    mongodao = MongoDao()
    db_conf = settings.CURRENT_DB_CONF
    res = mongodao.findAll(db_conf["CITY_TABLE"],{},projection)
    response_data['data']["cities"] = res
    response_data['data']["default"] = default_city 
    return JsonResponse(response_data)


def checkPODTOAndUpdate(po,dto):
    keys_to_compare = ["description" , "price" , "imageUrl"]
    to_return = {}
    to_return["ISUPDATED"] = False
    to_return["PO"] = po
    po_keys = po.keys()
    dto_keys = dto.keys()
    for key in keys_to_compare :
        if(key in ["imageUrl"]):
            for nestedKeyVal in dto[key]:
                if(nestedKeyVal not in po[key]):
                    po[key].append(nestedKeyVal)
                    to_return["ISUPDATED"] = True
        else:
            if(key in po_keys and key in dto_keys and po[key] != dto[key]):
                po[key] = dto[key]
                to_return["ISUPDATED"] = True
            elif(key not in po_keys and key in dto_keys):
                po[key] = dto[key]
                to_return["ISUPDATED"] = True
    return to_return
    

@csrf_exempt
def post_propertydata(request):
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {}
    request_body = request.body
    request_body = request_body.decode("utf-8")
    prop_dto = json.loads(request_body)
    if("property" not in prop_dto.keys() or prop_dto["property"] != 1):
        response_data['result'] = 'error'
        response_data['msg'] = 'input data is not property data'
        return JsonResponse(response_data)
    prop_key = gethashkeyofprop(prop_dto)
    mongodao = MongoDao()
    db_conf = settings.CURRENT_DB_CONF
    prop_po = mongodao.findByKey(db_conf["PROP_TABLE"],"prop_key",prop_key,False)
    if(prop_po is None):
        prop_dto["prop_key"] = prop_key
        prop_po = prop_dto
    else:
        prop_dto_keys = prop_dto.keys()
        ischanged = False
        is_updated_res = checkPODTOAndUpdate(prop_po , prop_dto)
        if(is_updated_res["ISUPDATED"] == False):
            response_data['result'] = 'error'
            response_data['msg'] = 'property exist'
            return JsonResponse(response_data)
        prop_po = is_updated_res["PO"]
    prop_po["screening"] = 0
    res = mongodao.insertpo(db_conf["PROP_TABLE"],prop_po)
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
