**Machine learning extension**
------------------------------
The machine learning extension performs the necessary machine learning 
applications for all other approaches. 
It consists of a small Flask server with REST endpoints. 

**Endpoints:**
To illustrate the functionality of the extension, 
we will take a closer look at each endpoint:

*/input*:
The input endpoint receives incoming data in the body of a POST request and stores it in a JSON file called data.json. 
This is currently used for the encryption extension.

*/federatedinput*:
The federatedinput endpoint receives data from the individual
clients in the distributed setup. This endpoint expects a 
'client' query parameter that passes the client number. 
This is important for saving the data for further use. The file is named according 
to the following scheme: 'model' + client + '.bin'.

*/fedavg*:
The fedavg endpoint aggregates the inputs
from the clients in the distributed setup
into a common new update. A query parameter
is expected to indicate how many client inputs
to wait for. Two hash maps described in the listener
extension can be used to count how many clients
have already responded. First, the system 
checks whether this number is greater than 
the query parameter, and if so, it reads the 
stored weight updates and calculates the average 
value using the weights. This is 
then stored in a file called "model.pt" for further use.

*/initialize*:
This endpoint stores the initialised model in order to return
it when this endpoint is requested. This means that the first 
model is distributed to the clients at the start of the 
distributed setup.

*/model*:
This endpoint returns the currently saved model.

*/learn*:
The learn endpoint performs classification on encrypted values.
To do this, the vectors and context must first be decoded. 
CKKS vectors can then be regenerated. Using the neural 
network defined in EncConvNet.py, the encrypted values are 
classified. The results are serialised and b64 encoded for 
transmission and cached.

*/prediction*:
The prediction endpoint serializes data and 
saves it as JSON in a file called "answer.json".

*/enc*:
This endpoint implements a way of classifying the encrypted data. 
Not currently used, only the learn endpoint.

*/output*:
The output endpoint returns the encrypted result as JSON.

*/data*:
The data endpoint provides the necessary model information for encryption, 
the kernel_shape and stride in the form of JSON.

*/predicted*:
The predicted endpoint shows a way to return the results. 
However, currently only the output endpoint is used.
