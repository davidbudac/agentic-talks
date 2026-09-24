package com.example.invoicing;

/** An amount or currency this package cannot handle. */
public class MoneyException extends IllegalArgumentException {

    public MoneyException(String message) {
        super(message);
    }
}
