package com.scsj4383.demo.controller;

import com.scsj4383.demo.service.CalculatorService;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Routes incoming HTTP requests to the CalculatorService and returns JSON.
 *
 * Endpoints (all GET):
 *   /                      -> health/info page
 *   /health                -> {"status":"UP"}
 *   /api/add?a=..&b=..     -> {"result": a+b}
 *   /api/subtract?a=..&b=..-> {"result": a-b}
 *   /api/multiply?a=..&b=..-> {"result": a*b}
 *   /api/divide?a=..&b=..  -> {"result": a/b}
 *   /api/prime?n=..        -> {"n":.., "prime": true/false}
 *   /api/fib?n=..          -> {"n":.., "fibonacci": ..}
 */
public class ApiHandler implements HttpHandler {

    private final CalculatorService service = new CalculatorService();

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        Map<String, String> query = parseQuery(exchange.getRequestURI().getRawQuery());

        String responseBody;
        int statusCode = 200;

        try {
            switch (path) {
                case "/":
                    responseBody = "{\"app\":\"SCSJ4383 DevOps Demo\",\"status\":\"UP\","
                            + "\"endpoints\":[\"/health\",\"/api/add\",\"/api/subtract\","
                            + "\"/api/multiply\",\"/api/divide\",\"/api/prime\",\"/api/fib\"]}";
                    break;
                case "/health":
                    responseBody = "{\"status\":\"UP\"}";
                    break;
                case "/api/add":
                    responseBody = "{\"result\":" + service.add(longParam(query, "a"), longParam(query, "b")) + "}";
                    break;
                case "/api/subtract":
                    responseBody = "{\"result\":" + service.subtract(longParam(query, "a"), longParam(query, "b")) + "}";
                    break;
                case "/api/multiply":
                    responseBody = "{\"result\":" + service.multiply(longParam(query, "a"), longParam(query, "b")) + "}";
                    break;
                case "/api/divide":
                    responseBody = "{\"result\":" + service.divide(longParam(query, "a"), longParam(query, "b")) + "}";
                    break;
                case "/api/prime":
                    long n = longParam(query, "n");
                    responseBody = "{\"n\":" + n + ",\"prime\":" + service.isPrime(n) + "}";
                    break;
                case "/api/fib":
                    int fn = (int) longParam(query, "n");
                    responseBody = "{\"n\":" + fn + ",\"fibonacci\":" + service.fibonacci(fn) + "}";
                    break;
                default:
                    statusCode = 404;
                    responseBody = "{\"error\":\"Not Found\"}";
            }
        } catch (IllegalArgumentException ex) {
            statusCode = 400;
            responseBody = "{\"error\":\"" + ex.getMessage() + "\"}";
        }

        byte[] bytes = responseBody.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    private long longParam(Map<String, String> query, String key) {
        String value = query.get(key);
        if (value == null) {
            throw new IllegalArgumentException("Missing required parameter: " + key);
        }
        try {
            return Long.parseLong(value);
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("Parameter " + key + " must be an integer");
        }
    }

    private Map<String, String> parseQuery(String rawQuery) {
        Map<String, String> result = new HashMap<>();
        if (rawQuery == null || rawQuery.isEmpty()) {
            return result;
        }
        for (String pair : rawQuery.split("&")) {
            int idx = pair.indexOf('=');
            if (idx > 0) {
                result.put(pair.substring(0, idx), pair.substring(idx + 1));
            }
        }
        return result;
    }
}
