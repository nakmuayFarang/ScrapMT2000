
# coding: utf-8

# In[4]:


import json, pymongo, os
from shutil import copyfile


# In[5]:


#setup pymong
from pymongo import MongoClient
client = MongoClient('localhost',27017 )
db = client.muayThaiResult
collection = db.mtFight


# In[7]:



error = list()
#insert in mongoDb documents
path = "./data/result/"
for file in os.listdir(path):
    if file != 'error':
        jsonFile = open(path + file,'r', encoding='utf-8')
        jsn = json.loads(jsonFile.read())
        jsonFile.close()
        try:
            collection.insert_one(jsn)
        except:
            print("Fail adding {} document".format(file))
            error.append(file)
            copyfile(path + file, path + 'error/' + file)


# In[23]:


file= error[3]
jsonFile = open(path + file,'r', encoding='utf-8')
jsn = json.loads(jsonFile.read())
jsonFile.close()


# In[24]:


collection.insert_one(jsn)

