from pymongo import MongoClient
from bson.json_util import dumps
import urllib.parse
import json
class MongoDao:
   'Common base class for all employees'
   empCount = 0

   def __init__(self,dbname):
       self.db = dbname
       self.url = 'mongodb://%s:%s@127.0.0.1/' % (urllib.parse.quote_plus(dbname), urllib.parse.quote_plus("leela@491")) + dbname
       self.mongoclient = MongoClient(self.url)
   

   def findAll(self,collection,condition,projection):
       collectionobj = self.mongoclient[self.db][collection]
       res = collectionobj.find(condition,projection)
       return json.loads(dumps(res))

   def findByKey(self,collection,key,val,outputjson=True):
       collectionobj = self.mongoclient[self.db][collection]
       res = collectionobj.find_one({key : val})
       if(outputjson == False):
           return res
       return json.loads(dumps(res))

   def insertpo(self,collection,mongopo):
       collectionobj = self.mongoclient[self.db][collection]
       return collectionobj.save(mongopo)

