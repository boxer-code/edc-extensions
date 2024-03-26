from cust import loadAnswer
import phe as paillier
from cust import getKeys
import os
import json

pfad = 'answer.json'
if os.path.exists(pfad):
    pub_key, priv_key = getKeys()
    answer_file=loadAnswer()
    answer_key=paillier.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = paillier.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    datafile = priv_key.decrypt(answer)
    if (answer_key==pub_key):
        with open('result.json', 'w') as file:
            json.dump(datafile, file)
            print(datafile)
    else:
        print("Es ist noch keine Antwort zum Entschlüsseln vorhanden.")
