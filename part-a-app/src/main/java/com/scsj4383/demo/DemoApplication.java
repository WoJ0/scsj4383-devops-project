package com.scsj4383.demo;

import com.scsj4383.demo.controller.ApiHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;

/**
 * Entry point for the SCSJ4383 DevOps demo service.
 *
 * Starts a lightweight HTTP server (JDK built-in, zero external dependencies) on
 * the port given by the PORT environment variable, defaulting to 8081.
 *
 * NOTE on ports: Jenkins itself runs on 8080 by default, so this demo app uses
 * 8081 to avoid a clash when both run on the same machine. The JMeter test plan
 * and Dockerfile use the same 8081.
 */
public class DemoApplication {

    public static void main(String[] args) throws IOException {
        int port = readPort();
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/", new ApiHandler());
        server.setExecutor(null); // default executor
        server.start();
        System.out.println("SCSJ4383 DevOps Demo started on http://localhost:" + port);
    }

    private static int readPort() {
        String env = System.getenv("PORT");
        if (env != null && !env.isEmpty()) {
            try {
                return Integer.parseInt(env);
            } catch (NumberFormatException ignored) {
                // fall through to default
            }
        }
        return 8081;
    }
}
