/*
 *  Copyright (c) 2021 Microsoft Corporation
 *
 *  This program and the accompanying materials are made available under the
 *  terms of the Apache License, Version 2.0 which is available at
 *  https://www.apache.org/licenses/LICENSE-2.0
 *
 *  SPDX-License-Identifier: Apache-2.0
 *
 *  Contributors:
 *       Microsoft Corporation - Initial implementation
 *
 */

package org.eclipse.edc.sample.extension.listener;

import org.eclipse.edc.connector.transfer.spi.observe.TransferProcessListener;
import org.eclipse.edc.connector.transfer.spi.types.TransferProcess;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.connector.transfer.spi.types.DataRequest;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class TransferProcessStartedListener implements TransferProcessListener {

    private final Monitor monitor;

    private static HashMap<String, String> ids = new HashMap<String, String>();

    private static HashMap<String, Boolean> checkIfPresent = new HashMap<String, Boolean>();

    public TransferProcessStartedListener(Monitor monitor) {
        this.monitor = monitor;
    }

    /**
     * Callback invoked by the EDC framework when a transfer is about to be completed.
     *
     * @param process the transfer process that is about to be completed.
     */
    @Override
    public void completed(final TransferProcess process) {
        monitor.debug("TransferProcessStartedListener received COMPLETED event");
        // do something meaningful before transfer start
        DataRequest address = process.getDataRequest();
        String connectoraddress = address.getConnectorAddress().toString();
        monitor.debug("Address " + connectoraddress);
        String contractId = address.getContractId().toString();
        monitor.debug("Contract Id " + address.getContractId().toString());
        // Jetzt Contract Id in Datei schreiben und Anzahl speichern
        if (ids.containsValue(connectoraddress) && !ids.containsKey(contractId)) {
            // Wenn der Schlüssel bereits vorhanden ist, erhöhe den Wert um 1
            // int currentValue = ids.get(contractId);
            // ids.put(connectoraddress, currentValue + 1);
            ids.put(contractId, connectoraddress);
            if (checkIfPresent.containsKey(connectoraddress)){
                checkIfPresent.replace(connectoraddress, true);
            }else{
                System.out.println("Es ist etwas schief gelaufen.");
            }
        } else if(!ids.containsValue(connectoraddress)){
            // Wenn der Schlüssel nicht vorhanden ist, füge ihn mit dem Wert 1 hinzu
            ids.put(contractId, connectoraddress);
            checkIfPresent.put(connectoraddress, false);
        }
        System.out.println("Map " + ids);
        System.out.println("Present " + checkIfPresent);
        String filename = "clients.txt";

        // Versuche, die Map in die Datei zu schreiben
        try {
            // Öffne eine BufferedWriter, um in die Datei zu schreiben
            BufferedWriter writer = new BufferedWriter(new FileWriter(filename));

            // Schreibe jeden Eintrag der Map in die Datei
            for (Map.Entry<String, String> entry : ids.entrySet()) {
                writer.write(entry.getKey() + ": " + entry.getValue());
                writer.newLine(); // Füge eine neue Zeile hinzu
            }

            // Schließe den BufferedWriter
            writer.close();

            System.out.println("Die Map wurde erfolgreich in die Datei '" + filename + "' geschrieben.");
        } catch (IOException e) {
            System.err.println("Fehler beim Schreiben der Datei: " + e.getMessage());
        }
   }

}
