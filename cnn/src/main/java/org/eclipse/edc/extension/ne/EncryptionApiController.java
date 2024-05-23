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

package org.eclipse.edc.extension.ne;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jep.Interpreter;
import jep.JepConfig;
import jep.JepException;
import jep.SharedInterpreter;
import org.eclipse.edc.spi.monitor.Monitor;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;
//import static jep.MainInterpreter.setInitParams;

@Produces({MediaType.APPLICATION_JSON})
@Path("/")
public class EncryptionApiController {

    private static String pfad = null;
    private static int confi = 0;
    private static HashMap da = null;

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

    public static HashMap runScript(String datei, String mode) throws JepException {
        //PyConfig pyConfig = new PyConfig();
        //pyConfig.setPythonHome("/home/kuhlmann/.local/lib/python3.10");
        //jep.JepConfig jepConf = new JepConfig();

        //jepConf.addIncludePaths(pfad);

        //jepConf.addIncludePaths(pythonFolder);

        //SharedInterpreter.setConfig(jepConf);
        //try {
        //setInitParams(pyConfig);
        //} catch (JepException e) {
        //e.printStackTrace();
        //}
        configset(pfad);
        try (Interpreter interp = new SharedInterpreter()) {
            String scriptPath = pfad + datei;
            //interp.setConfig(jepConf);
            interp.runScript(scriptPath);
            if (mode.equals("input")) {
                Object context = interp.getValue("ctx");
                Object vectors = interp.getValue("data");
                Object windows = interp.getValue("windows");
                String serctx = context.toString();
                String enc = vectors.toString();
                HashMap<String, Object> datavec = new HashMap<>();

                // Fügen Sie die Werte zum Map-Objekt hinzu
                datavec.put("ckks_vector", vectors);
                datavec.put("context", context);
                datavec.put("windows", windows);
                //System.out.println("Erfolgreich hier angekommen!");
                return datavec;
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
    @Path("data")
    public String datarequest() throws JepException {
        //configset();
        String pathcomplete = "/data.py";
        runScript(pathcomplete, "data");
        return "Datarequest successfull!";
    }

    @GET
    @Path("input")
    public String enc() throws JepException {
        //configset();
        String pathcomplete = "/encryption.py";
        HashMap daenc = runScript(pathcomplete, "input");
        da = daenc;
        return "Success";
    }

    @GET
    @Path("enc")
    public HashMap ret() {
        if (da.equals(null)) {
            System.out.println("Bitte erst mit input Daten initialisieren");
        } else {
            return da;
        }
        return null;
    }

    @POST
    @Consumes({MediaType.APPLICATION_OCTET_STREAM})
    @Path("encrypted")
    public String dec(byte[] body) throws JepException {
        //configset();
        //String res = new String(body, StandardCharsets.UTF_8);
        File file = new File("result.txt"); //Datei, in die geschrieben werden soll
        try {
            FileOutputStream writer = new FileOutputStream(file); //Erzeugen eines effizienten Writers für Textdateien
            writer.write(body);
        } catch (IOException e) {
            // Handle Ausnahmen entsprechend...
            e.printStackTrace();
        }
        return "Received encrypted results!";
    }

    @POST
    @Consumes({MediaType.APPLICATION_OCTET_STREAM})
    @Path("kernel")
    public String ker(byte[] body) throws JepException {
        //configset();
        //String res = new String(body, StandardCharsets.UTF_8);
        File file = new File("kernel.txt"); //Datei, in die geschrieben werden soll
        try {
            FileOutputStream writer = new FileOutputStream(file); //Erzeugen eines effizienten Writers für Textdateien
            writer.write(body);
        } catch (IOException e) {
            // Handle Ausnahmen entsprechend...
            e.printStackTrace();
        }
        return "Received data from model!";
    }

    @GET
    @Path("decrypt")
    public String de() throws JepException {
        String pathcomplete = "/decryption.py";
        runScript(pathcomplete, "decrypt");
        return "Successfully decrypted";
    }

    @GET
    @Path("output")
    public String out() throws JepException {
        String pathcomplete = "/out.py";
        runScript(pathcomplete, "out");
        return "Writing output to file done!";

    }

}
