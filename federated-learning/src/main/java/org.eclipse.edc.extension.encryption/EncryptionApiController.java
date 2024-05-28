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

package org.eclipse.edc.extension.encryption;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jep.Interpreter;
import jep.JepConfig;
import jep.JepException;
import jep.SharedInterpreter;
import org.eclipse.edc.spi.monitor.Monitor;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;

@Produces({MediaType.APPLICATION_JSON})
@Path("/")
public class EncryptionApiController {

    private static int confi = 0;
    private static final HashMap DA = null;

    private static String pfad = null;
    private static byte[] dump = null;

    public static void configset(String path) throws JepException {
        if (confi == 0) {
            jep.JepConfig jepConf = new JepConfig();

            jepConf.addIncludePaths(path);

            //jepConf.addIncludePaths(pythonFolder);

            SharedInterpreter.setConfig(jepConf);
            confi = confi + 1;
        } else {
            System.out.println("Config is already set");
        }
    }

    public static String runScript(String datei, String mode) throws JepException {
        configset(pfad);
        try (Interpreter interp = new SharedInterpreter()) {
            String scriptPath = pfad + datei;
            interp.runScript(scriptPath);
        } catch (JepException e) {
            System.out.println(e.getMessage());

            /* Hier geben wir die Aufruferliste aus */
            e.printStackTrace();
        }
        return null;
    }

    public static String runScript(String datei, String mode, String[] values) throws JepException {
        configset(pfad);
        try (Interpreter interp = new SharedInterpreter()) {
            String scriptPath = pfad + datei;
            interp.set("javaValues", List.of(values[0], values[1], values[2], values[3]));
            interp.runScript(scriptPath);
            if (mode.equals("input")) {
                Object serialisied = interp.getValue("datafile");
                String jsonString = serialisied.toString();
                JsonObject jsonObject = JsonParser.parseString(jsonString).getAsJsonObject();
                return jsonString;
            }
        } catch (JepException e) {
            System.out.println(e.getMessage());

            /* Hier geben wir die Aufruferliste aus */
            e.printStackTrace();
        }
        return null;
    }

    private final Monitor monitor;

    public EncryptionApiController(Monitor monitor) {
        this.monitor = monitor;
    }


    @POST
    @Consumes({MediaType.APPLICATION_OCTET_STREAM})
    @Path("input")
    public String learn(byte[] body) {
        File file = new File("model.pt"); //Datei, in die geschrieben werden soll
        try {
            FileOutputStream writer = new FileOutputStream(file); //Erzeugen eines Writers für Textdateien
            writer.write(body);
        } catch (IOException e) {
            // Handle Ausnahmen entsprechend...
            e.printStackTrace();
        }
        return "Received model";
    }

    @GET
    @Path("train")
    public byte[] train() throws JepException, IOException {
        String datei = "/training.py";
        runScript(datei, "train");
        System.out.println("Trained model locally");
        //Einlesen des Modells und abspeichern in der Variablen
        String fileName = "model.pt";
        byte[] bytes = Files.readAllBytes(java.nio.file.Path.of(fileName));
        dump = bytes;
        System.out.println(dump);
        return dump;
    }

    @GET
    @Path("update")
    public byte[] up() throws JepException {
        return dump;
    }


    @POST
    @Path("config")
    public String config(String path) throws JepException {
        pfad = path;
        configset(path);
        return "JepConfig is set";
    }

    @GET
    @Path("health")
    public String checkHealth() {
        monitor.info("Received a health request");
        return "{\"response\":\"I'm alive!\"}";
    }

    @GET
    @Path("encryption")
    public String enc(@QueryParam("values") @DefaultValue("44,4,6,1") String values) throws JepException {
        String datei = "/encrypt_data.py";
        String[] arrSplit = values.split(",");
        System.out.println(arrSplit[0] + arrSplit[1] + arrSplit[2] + arrSplit[3]);
        String encryptedData = runScript(datei, "input", arrSplit);
        System.out.println("Die angefragten Daten wurden verschlüsselt.");
        return encryptedData;
    }

    @POST
    @Consumes({MediaType.APPLICATION_OCTET_STREAM})
    @Path("encrypted")
    public String dec(byte[] body) throws JepException {
        //configset();
        //String res = new String(body, StandardCharsets.UTF_8);
        File file = new File("answer.json"); //Datei, in die geschrieben werden soll
        try {
            FileOutputStream writer = new FileOutputStream(file); //Erzeugen eines Writers für Textdateien
            writer.write(body);
        } catch (IOException e) {
            // Handle Ausnahmen entsprechend...
            e.printStackTrace();
        }
        return "Received encrypted results!";
    }

    @GET
    @Path("decrypt")
    public String de() throws JepException {
        String datei = "/decrypt_answer.py";
        runScript(datei, "decrypt");
        return "Successfully decrypted";
    }

}