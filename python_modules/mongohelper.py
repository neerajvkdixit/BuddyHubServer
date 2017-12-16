from pymongo import MongoClient
from bson.json_util import dumps
import urllib.parse
import json
from django.conf import settings
class MongoDao:
   'Common base class for all employees'
   empCount = 0

   def __init__(self):
       db_conf = settings.CURRENT_DB_CONF
       print(db_conf)
       self.url = 'mongodb://'+urllib.parse.quote_plus(db_conf["USER"])+':'+urllib.parse.quote_plus(db_conf["PASSWORD"]) +'@'+db_conf["DBURL"]
       print(self.url)
       #self.url = 'mongodb://%s:%s@'+db_conf["DBURL"]+'/' % (urllib.parse.quote_plus(db_conf["DBNAME"]), urllib.parse.quote_plus(db_conf["PASSWORD"])) + db_conf["DBNAME"]
       self.mongoclient = MongoClient(self.url)
   

   def findAll(self,collection,condition,projection):
       db_conf = settings.CURRENT_DB_CONF
       collectionobj = self.mongoclient[db_conf["DBNAME"]][collection]
       res = collectionobj.find(condition,projection)
       return json.loads(dumps(res))

   def findByKey(self,collection,key,val,outputjson=True):
       db_conf = settings.CURRENT_DB_CONF
       collectionobj = self.mongoclient[db_conf["DBNAME"]][collection]
       res = collectionobj.find_one({key : val})
       if(outputjson == False):
           return res
       return json.loads(dumps(res))

   def insertpo(self,collection,mongopo):
       db_conf = settings.CURRENT_DB_CONF
       collectionobj = self.mongoclient[db_conf["DBNAME"]][collection]
       return collectionobj.save(mongopo)

