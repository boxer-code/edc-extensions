import requests
from flask import *
from base64 import b64encode, b64decode
import tenseal as ts
from EncConvNet import *
import Service as se
from training import *
from servercalc import serializeData
import state as s
import os
import json
import pickle
import io
import time
from collections import Counter

app = Flask(__name__)

@app.post("/input")
def enc():
    global req
    req = request.get_json(force=True)
    with open('data.json', 'w') as file:
        json.dump(req, file)
    return ("Successfully received data")

@app.post("/federatedinput")
def fed():
    client = request.args.get('client')
    global req
    req = request.get_data()
    filename = 'model' + client + '.bin'
    with open(filename, 'wb') as f:
        f.write(req)
    return ("Successfully received updated model")

@app.get("/fedavg")
def avg():
    print("Warten auf Registrierung genügender Clients.")
    clients = request.args.get('clients')
    given = count()
    if len(given) < int(clients):
        return "Es sind noch nicht genügend Updates von Clients eingetroffen."
    else:
        models = []
        print(len(given))
        for i in range(1, len(given)+1):
            #Hier Daten der Modelle einlesen und Gewichte extrahieren. Modelle sind mit model_bytes "Nummer des Clienten" nummeriert. Also kann durchgegangen werden bis zu "Clients"
            #with (open("model" + str(i) + ".bin", "rb")) as f:
            #    pickload = pickle.load(f)
            #buffer = io.BytesIO()
            #torch.save(pickload, buffer)

            # Setze die Position des Puffers auf den Anfang
            #buffer.seek(0)

            # Lade das Modell aus dem Puffer
            #loaded_model = torch.load(buffer, map_location=torch.device('cpu'))
            #model = torch.load(pickload)
            with open("model" + str(i) + ".bin", "rb") as f:
                model_bytes = f.read()
            # 2. Lade das Modell aus den Bytes
            loaded_model = torch.load(io.BytesIO(model_bytes))
            models.append(loaded_model)
            print(i)
            print(loaded_model)

        average_weights = {}
        for param_name in models[0].keys():
            average_weights[param_name] = torch.stack([weights[param_name] for weights in models]).mean(dim=0)
        print("Average")
        print(average_weights)
        average_model = ConvNet()
        average_model.load_state_dict(average_weights)
        torch.save(model.state_dict(), "model.pt")
        dumped = pickle.dumps(model.state_dict())
        return "Es wurde erfolgreich ein geupdatetes Model erzeugt!"

#Erst in Datei und dann noch ein Endpunkt zum Verschicken
@app.get("/initialize")
def modeltest():
    print(model)
    torch.save(model.state_dict(), "model.pt")
    global dumped
    dumped = pickle.dumps(model.state_dict())
    #pickload = pickle.loads(dumped)
    #buffer = io.BytesIO()
    #torch.save(pickload, buffer)

    # Setze die Position des Puffers auf den Anfang
    #buffer.seek(0)

    # Lade das Modell aus dem Puffer
    #loaded_model = torch.load(buffer, map_location=torch.device('cpu'))
    #loaded = torch.load(pickload)
    #print(loaded_model)
    return ("Model ist initialisiert.")

@app.get("/model")
def getmodel():
    #Jedes Mal wenn das Model angefordert wird, wird von einem neuen Client ausgegangen
    return dumped

@app.get("/learn")
def learn():
    data = req
    vectors = []
    #Jeden Vektor wieder b64 dekodieren
    for d in data['ckks_vector']: 
        ck_vector = b64decode(d)
        vectors.append(ck_vector)
    window = data['windows']
    #Kontext dekodieren
    ctx = b64decode(data['context'])
    #Kontext deserialisieren
    ctx_d = ts.context_from(ctx)
    enc_v = []
    #Rekonstruieren der Vektoren
    for vec in vectors:
       enc_vec = ts.ckks_vector_from(ctx_d, vec) 
       enc_v.append(enc_vec)
    print("<p>There are vectors again!</p>")
    #Liste mit verschlüsselten Vektoren env_v
    enc_model = EncConvNet(model)
    print(enc_model)
    enc_learned = se.enc_test(enc_v, enc_model, window)
    learned =[]
    for enc in enc_learned:
        vec = enc.serialize()
        vec_new = b64encode(vec).decode()
        learned.append(vec_new)
    
    data = {
        "learned_data": learned, 
        "context" : data['context']
    }
    global encrypted_result
    encrypted_result = data
    print("<p>Successfully learned and ready to send back the data!</p>")
    return data

@app.get("/prediction")
def pred():
    if os.path.exists('data.json'):
        datafile=serializeData()
        with open('answer.json', 'w') as file:
            json.dump(datafile, file)
        return ("Die Vorhersage wurde abgespeichert.")
    else:
        print("Es sind noch keine Daten zur Auswertung verfügbar.")


@app.post("/enc")
def enc_p():
    data = request.get_json()
    vectors = []
    #Jeden Vektor wieder b64 dekodieren
    for d in data['ckks_vector']: 
        ck_vector = b64decode(d)
        vectors.append(ck_vector)
    #Kontext dekodieren
    ctx = b64decode(data['context'])
    #Kontext deserialisieren
    ctx_d = ts.context_from(ctx)
    enc_v = []
    #Rekonstruieren der Vektoren
    for vec in vectors:
       enc_vec = ts.ckks_vector_from(ctx_d, vec) 
       #enc_vec.decrypt()
       enc_v.append(enc_vec)
    #Liste mit verschlüsselten Vektoren env_v
    enc_model = EncConvNet(model)
    enc_learned = enc_test(enc_v, enc_model)
    learned =[]
    for enc in enc_learned:
        vec = enc.serialize()
        vec_new = b64encode(vec).decode()
        learned.append(vec_new)
    
    data = {
        "learned_data": learned
    }
    print("<p>Successfully learned and ready to send back the data!</p>")
    return data

@app.get("/test")
def enc_lr():
    with open('data.json', 'r') as file:
        ans=json.load(file)
    enc_model = EncConvNet(model)
    enc_learned = enc_test(ans, enc_model)
    return "Hier"

@app.get("/output")
def out():
    try:
        if encrypted_result != None:
            return jsonify(encrypted_result)
    except AttributeError as e:
        print("Error occured")

@app.get("/data")
def da():
    print("Data request received.")
    data = {
        "kernel_shape": kernel_shape,
        "stride" : stride
    }
    return data

@app.get("/predicted")
def p():
    try:
        if os.path.exists('answer.json'):
            with open('answer.json', 'r') as file:
                d=json.load(file)
            #data=json.loads(d)
            return d

    except AttributeError as e:
        print("Error occured")

def count():
    data_dict = {}
    with open('../clients.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Zeilen in Schlüssel und Wert trennen
            key, value = line.strip().split(': ')
            # Schlüssel-Wert-Paar zum Dictionary hinzufügen
            data_dict[key] = value
    frequency_counter = Counter(data_dict.values())
    # Ausgabe der Häufigkeit
    print(frequency_counter)
    return frequency_counter

kernel_shape = model.conv1.kernel_size
stride = model.conv1.stride[0]
counter = 1
app.run(host='0.0.0.0', port=7000)
