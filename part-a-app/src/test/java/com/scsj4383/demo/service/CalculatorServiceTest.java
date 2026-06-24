package com.scsj4383.demo.service;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Unit tests for CalculatorService. These run during the Jenkins "Test" stage
 * (mvn test) and the results are published to the pipeline.
 */
class CalculatorServiceTest {

    private final CalculatorService service = new CalculatorService();

    @Test
    void add_returnsSum() {
        assertEquals(5, service.add(2, 3));
        assertEquals(-1, service.add(2, -3));
    }

    @Test
    void subtract_returnsDifference() {
        assertEquals(-1, service.subtract(2, 3));
    }

    @Test
    void multiply_returnsProduct() {
        assertEquals(6, service.multiply(2, 3));
        assertEquals(0, service.multiply(0, 99));
    }

    @Test
    void divide_returnsQuotient() {
        assertEquals(2.5, service.divide(5, 2), 1e-9);
    }

    @Test
    void divide_byZero_throws() {
        assertThrows(IllegalArgumentException.class, () -> service.divide(5, 0));
    }

    @Test
    void isPrime_identifiesPrimes() {
        assertTrue(service.isPrime(2));
        assertTrue(service.isPrime(13));
        assertTrue(service.isPrime(7919));
        assertFalse(service.isPrime(1));
        assertFalse(service.isPrime(15));
    }

    @Test
    void fibonacci_returnsExpectedValues() {
        assertEquals(0, service.fibonacci(0));
        assertEquals(1, service.fibonacci(1));
        assertEquals(55, service.fibonacci(10));
    }

    @Test
    void fibonacci_negative_throws() {
        assertThrows(IllegalArgumentException.class, () -> service.fibonacci(-1));
    }
}
