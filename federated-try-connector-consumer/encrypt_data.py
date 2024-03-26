from cust import getKeys
from cust import serializeData
from cust import storeKeys
import os
import json

dateipfad = 'custkeys.json'

if os.path.exists(dateipfad):
    print("Es wurden bereits Schlüssel erstellt.")
else:
    storeKeys()
    print("Schlüssel wurden neu erstellt.")

pub_key, priv_key = getKeys()
element_list = javaValues
print(element_list)
data = [int(element) for element in element_list]
#data = age, he, al, gen = [44,4,6,1]
serializeData(pub_key, data)
global datafile
datafile=serializeData(pub_key, data)
with open('data.json', 'w') as file:
    json.dump(datafile, file)
