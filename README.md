Welcome to the MeLtcryption edc extensions repository!

This repository should contain custom extensions developed for the "Eclipse Dataspace Connector" to enhance the functionality for privacy preserving machine learning. As this repository represents the initial transition of custom extensions from a private development environment to a public repository, so far only the extension for federated learning has been developed and transferred far enough and is presented here. 

**Quick start**
--------------------------------
Make sure that Java 17 is installed and the JAVA__HOME variable is set correctly.
jep (https://github.com/ninia/jep) has to be installed. If not, *pip install jep*.

**Federated learning Setup**
-------------------
The setup contains one server whichs serves as a federator and initiliazes the net and distributes it to the clients. The training process takes place on client side. Afterwards the updated weights are sent to the server, which aggregates the weights and send the average as a new model back to the clients. 
Our test-scenario contains two clients but is easy to extend if more clients are needed. The client is initialize with a first net from the server and the training takes place locally.
To show the functionality of this extension we are using a small convolutional net with 3 layers. 

Setup start:
1. Clone this repository two times.
2. cd edc-extensions
3. To build the jar-files: ./gradlew clean federated-try-connector:build
4. To start the first consumer connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/edc-extensions/federated-try-connector/consumer.properties  -jar cnn/build/libs/filesystem-config-connector.jar
5. (In a new terminal window) To start the second consumer connector the second repository is needed: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/edc-extensions2/federated-try-connector/consumer2.properties  -jar cnn/build/libs/filesystem-config-connector.jar
6. (In a new terminal window) To start the provider connector: java -Djava.library.path={path to jep installation] -Dedc.fs.config=/{path to cloned repo}/edc-extensions/federated-try-connector/provider.properties  -jar cnn/build/libs/filesystem-config-connector.jar
7. (In a new terminal window) cd Machine-Learning
8. To start the ML-Service: python3 ML.py

Transfer steps:
1. Data encryption: curl --location 'http://localhost:8181/api/input'
2. Data offering with encrypted data: [Postman script for encryption](cnn/postman-encryption.json)
3. Classification of encrypted values: curl --location 'http://localhost:7000/learn'
4. Data offering with encrypted results: [Postman script for decryption](cnn/postman-decryption.json)
5. Decryption: curl --location 'http://localhost:8181/api/decrpyt'

Results are stored in result_learning.txt.

**Configuration**

*Connector*:
For the setup the Eclipse Dataspace Connector is used (https://github.com/eclipse-edc/Connector). It is extended with the control plane, data plane, configuration, management extension which provide the possibility for configuration. 
In our Setup the consumer connector is configured with [consumer.properties](connector-extension/consumer.properties) and the provider connector with [provider.properties](connector-extension/provider.properties).
The extension for encryption is managed by the *web.http.port* and the *web.http.path*. 

*Encryption*:
In [App.py](connector-extension/src/main/java/org/eclipse/edc/extension/health/App.py) the number of random MNIST-Values is configured. As default 500 values should be encrypted. 
*Machine-Learning*: TODO
