**Quick start**
--------------------------------
Make sure that Java 17 is installed and the JAVA__HOME variable is set correctly.
jep (https://github.com/ninia/jep) has to be installed. If not, *pip install jep*.

**CNN Setup**
-------------------
To perform the encryption TenSeal (https://github.com/OpenMined/TenSEAL) is used.

Setup start:
1. Clone this repository.
2. cd SiDaKo-EDC
3. To build the jar-files: ./gradlew clean cnn:build
4. To start the consumer connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/SiDaKo-EDC/cnn/consumer.properties  -jar cnn/build/libs/filesystem-config-connector.jar
5. To start the provider connector: java -Djava.library.path={path to jep installation] -Dedc.fs.config=/{path to cloned repo}/SiDaKo-EDC/cnn/provider.properties  -jar cnn/build/libs/filesystem-config-connector.jar
6. cd Machine-Learning
7. To start the ML-Service: python3 ML.py

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

**Linear-Regression**
-------------------
To perform the encryption the palliere encryption system is used. 

Setup start: 
1. Clone this repository.
2. cd SiDaKo-EDC
4. To build the jar-files: ./gradlew clean linear-regression:build
5. To start the consumer connector: java -Djava.library.path={path to jep installation} -Dedc.fs.config={path to cloned repo}/SiDaKo-EDC/linear-regression/consumer.properties  -jar linear-regression/build/libs/filesystem-config-connector.jar
6. To start the provider connector: java -Djava.library.path={path to jep installation] -Dedc.fs.config={path to cloned repo}/SiDaKo-EDC/linear-regression/provider.properties  -jar linear-regression/build/libs/filesystem-config-connector.jar
7. cd Machine-Learning
8. To start the ML-Service: python3 Classifier.py

Transfer steps:
1. Data encryption: [Postman script for encryption](linear-regression/encryption-lr.postman_collection.json)
2. Data decrytion: [Postman script for decryption](linear-regression/decryption-lr.postman_collection.json)

**Configuration**:
You need to adapt the path to the python files in the bhody of the first request of the encryption script to your own file-system. The to-be-encrypted-data is configured by parametrisation of the access-url from the asset holding the encrypted data. 
