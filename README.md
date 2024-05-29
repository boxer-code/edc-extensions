Welcome to the MeLtcryption edc extensions repository!

This repository should contain custom extensions developed for the "Eclipse Dataspace Connector" to enhance the functionality for privacy-preserving machine learning. As this repository represents the initial transition of custom extensions from a private development environment to a public repository, only the extension for federated learning and encrypted machine learning with a simple CNN has been developed and transferred far enough for presentation. 

**Quick start**
--------------------------------
Make sure that Java 17 is installed and the JAVA__HOME variable is set correctly.
jep (https://github.com/ninia/jep) has to be installed. If not, *pip install jep*.

Setup start:

1. Clone this repo (for the federated setup you need to clone the repo two times, in a real world scenario clients would be on different machines).
2. cd edc-extensions
3. Build the jar-files: ./gradlew clean federated-learning:build (federated setup), ./gradlew clean cnn:build (encrypted machine learning setup)
4. Detailed instructions for further steps in [federated setup](federated-learning), [encryption setup](cnn).



