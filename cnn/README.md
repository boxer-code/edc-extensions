**Encryption Setup (CNN)**
-------------------
To perform the encryption TenSeal (https://github.com/OpenMined/TenSEAL) is used.

Setup start:
1. To start the consumer connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config=/{path to cloned repo}/edc-extensions-self/cnn/consumer.properties  -jar cnn/build/libs/filesystem-config-connector.jar
2. To start the provider connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config=/{path to cloned repo}/edc-extensions-self/cnn/provider.properties  -jar cnn/build/libs/filesystem-config-connector.jar
3. cd Machine-Learning
4. To start the ML-Service: python3 ML.py
5. Set-up the postman jep variable: If you want to use postman for the next steps, you have to set the pfadjep variable to your path to the python files (something like: {path to cloned repo}/SiDaKo-EDC/cnn/src/main/java/org/eclipse/edc/extension/ne).

Transfer steps:
1. Transferring the necessary informations about the model to the data provider: [Postman script for model informations](Information-about-model.postman_collection.json)
1. Data encryption: [Postman script for encryption](http-http-encryption.postman_collection.json)
2. Encrypted Machine-Learning and decryption: [Postman script for decryption](http-http-decryption.postman_collection.json)

Results are stored in result_learning.txt.

**Configuration**

*Connector*:
For the setup the Eclipse Dataspace Connector is used (https://github.com/eclipse-edc/Connector). It is extended with the control plane, data plane, configuration, management extension which provide the possibility for configuration. 
In our Setup the consumer connector is configured with [consumer.properties](cnn/consumer.properties) and the provider connector with [provider.properties](cnn/provider.properties).
The extension for encryption is managed by the *web.http.port* and the *web.http.path*. 

*Encryption*:
In [App.py](cnn/src/main/java/org/eclipse/edc/extension/health/App.py) the number of random MNIST-Values is configured. As default 500 values should be encrypted. 

*Machine-Learning*: TODO
