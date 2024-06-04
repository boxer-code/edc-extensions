**Listener for federated learning**
------------------------------------
For distributed learning, the service provider needs information about how many models have already been requested and 
whether it has received a response from the requesters. This is done in our distributed learning extension via another 
extension that reacts to completed transfer processes. Before a transfer is started, a contract is established under a 
unique contract UIID. Once a transfer is complete, the connector's address is entered into a hash map together with the 
contract UIID.  The value is the contract UIID and the key is the connector address. If the requesting connector has 
requested for the first time, the address and a false are also entered into a second hash map. This indicates that the 
connector has already requested the model. If the same connector now responds with the updates, a new contract is 
made and a second entry is made in the first hash map. The next step is to check if the connector is requesting for the 
first time or if it already has two entries with different contract UUIDS. If the latter is the case, the entry in the 
second hash map is set to true, indicating that there have been two communication paths between the connectors 
and that the updates have been successfully sent, as currently defined.