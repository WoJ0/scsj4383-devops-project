package com.scsj4383.demo.service;

/**
 * Core business logic for the demo REST API.
 *
 * Kept dependency-free so the service can be unit-tested in isolation and so the
 * whole project builds into a single runnable JAR with no external libraries.
 */
public class CalculatorService {

    public long add(long a, long b) {
        return a + b;
    }

    public long subtract(long a, long b) {
        return a - b;
    }

    public long multiply(long a, long b) {
        return a * b;
    }

    public double divide(long a, long b) {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed");
        }
        return (double) a / b;
    }

    /**
     * Returns true if {@code n} is a prime number.
     * Deliberately a little compute-heavy so JMeter load tests show a measurable response time.
     */
    public boolean isPrime(long n) {
        if (n < 2) {
            return false;
        }
        for (long i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * Returns the n-th Fibonacci number (iterative, O(n)).
     */
    public long fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }
        long previous = 0;
        long current = 1;
        for (int i = 0; i < n; i++) {
            long next = previous + current;
            previous = current;
            current = next;
        }
        return previous;
    }
}
