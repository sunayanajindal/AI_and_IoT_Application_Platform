import random
stats = []
n = 4
for i in range(n):
    available_RAM = random.random()*20
    idle = random.random()*20
    stats.append([available_RAM,idle])
    
for i in range(n):
    print(stats[i][0],stats[i][1])
stats.sort()

i = 0
while i<n-1 and stats[i][0] == stats[i+1][0]:
        i += 1
        
print(stats[0])   

from pymongo import MongoClient

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

dbname = client['AI_PLATFORM']

col = dbname["node"]
op = col.inventory.find( {} )
for x in op:
  print(x)
  