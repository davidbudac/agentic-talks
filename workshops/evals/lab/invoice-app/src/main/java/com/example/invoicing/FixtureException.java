package com.example.invoicing;

/** A fixture file that cannot be used, with the row number when it is known. */
public class FixtureException extends RuntimeException {

    public FixtureException(String message) {
        super(message);
    }

    public FixtureException(String message, Throwable cause) {
        super(message, cause);
    }
}
