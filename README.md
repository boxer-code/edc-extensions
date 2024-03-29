Welcome to the MeLtcryption edc extensions repository!

This repository should contain custom extensions developed for the "Eclipse Dataspace Connector" to enhance the functionality for privacy preserving machine learning. As this repository represents the initial transition of custom extensions from a private development environment to a public repository, so far only the extension for federated learning has been developed and transferred far enough and is presented here. 

**Quick start**
--------------------------------
Make sure that Java 17 is installed and the JAVA__HOME variable is set correctly.
jep (https://github.com/ninia/jep) has to be installed. If not, *pip install jep*.

**Federated learning Setup**
-------------------
The setup contains one server which serves as a federator and initializes the net and distributes it to the clients. The training process takes place on the client side. Afterwards the updated weights are sent to the server, which aggregates the weights and sends the average as a new model back to the clients. 
Our test-scenario contains two clients but is easy to extend if more clients are needed. The client is initialized with a first net from the server and the training takes place locally.
To show the functionality of this extension we are using a small convolutional net with 3 layers. 

Setup start:
1. Clone this repository two times (in a real world scenario clients would be on different machines).
2. cd edc-extensions
3. To build the jar-files: ./gradlew clean federated-try-connector:build
4. To start the first consumer connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/edc-extensions/federated-try-connector/consumer.properties  -jar federated-try-connector/build/libs/filesystem-config-connector.jar
5. (In a new terminal window) To start the second consumer connector the second repository is needed: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/edc-extensions2/federated-try-connector/consumer2.properties  -jar federated-try-connector/build/libs/filesystem-config-connector.jar
6. (In a new terminal window) To start the provider connector: java -Djava.library.path={path to jep installation] -Dedc.fs.config=/{path to cloned repo}/edc-extensions/federated-try-connector/provider.properties  -jar federated-try-connector/build/libs/filesystem-config-connector.jar
7. (In a new terminal window) cd Machine-Learning
8. To start the ML-Service: python3 ML.py

Transfer steps:
To perform two rounds of federated learning a postman collection is given ([postman collection for two rounds of federated learning](federated-try-connector/Federated-learning-two-rounds.postman_collection.json)). First you have to adapt the "pfadjep" variable to your full path to the python files. For example: "/home/{User}/edc-extensions-self/federated-try-connector". If you want to run the whole collection, you should set the delay to 2000ms.
The first requests are to initialize the model on the server side and to set the jep config on both clients. Afterwards a data offering is created and all the necessary structures for it. The clients negotiate a contract with the server and download the first model. Afterwards they train it and create another data offering, containing the model updates. The server negotiates a contract with the clients and gets the model updates to average them and send them back through a data offering. The contracts can be reused for more rounds of federated learning. Also the collection can simply run another round. 

**Configuration**

*Clients*:
To extend the scenario with more clients, at the current state you have to clone the repository for each client. The clients are numbered and the number is transferred to the server as a variable. If you want to change the number or add more clients you have to adapt the body of the "Start the transfer Copy" request. The base-url contains the number. For example: "baseUrl": "http://localhost:7000/federatedinput?client=1". How many feedbacks the server should receive before averaging is set in the "/fedavg" request. For example: "http://localhost:7000/fedavg?clients=2".

*Connector*:
For the setup the Eclipse Dataspace Connector is used (https://github.com/eclipse-edc/Connector). It is extended with the control plane, data plane, configuration, and management extension which provides the possibility for configuration. 
In our setup the first consumer connector is configured with [consumer.properties](federated-try-connector/consumer.properties), the second consumer connector is configured with [consumer2.properties](federated-try-connector/consumer2.properties) and the provider connector with [provider.properties](federated-try-connector/provider.properties).
The federated-learning extension is managed by the *web.http.port* and the *web.http.path*. 

*Machine learning*:
In the future it should be possible to fully exchange the model without any big modifications. At the current stage we haven't tried to change the model. It is specified in [convnet.py](federated-try-connector/convnet.py). The training is specified in [training.py](federated-try-connector/training.py).
