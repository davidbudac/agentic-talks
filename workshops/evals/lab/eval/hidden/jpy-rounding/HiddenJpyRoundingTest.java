package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Hidden acceptance tests for task jpy-rounding. The agent never sees this file. */
class HiddenJpyRoundingTest {

    private static BigDecimal d(String value) {
        return new BigDecimal(value);
    }

    @Test
    void roundsHalfUpToWholeYen() {
        assertEquals(d("1235"), Money.round(d("1234.5"), "JPY"));
        assertEquals(d("1234"), Money.round(d("1234.4"), "jpy"));
    }

    @Test
    void formatsWithoutDecimals() {
        assertEquals("1,235 JPY", Money.format(d("1234.5"), "JPY"));
    }

    @Test
    void allocatesWholeYen() {
        assertEquals(List.of(d("34"), d("33"), d("33")), Money.allocate(d("100"), 3, "JPY"));
    }

    @Test
    void grossInYen() {
        assertEquals(d("1100"), Invoices.gross(d("1000"), d("0.10"), "JPY"));
        assertEquals(d("1100"), Invoice.of("J-1", "Osaka KK", "1000", "0.10", "jpy").gross());
    }

    @Test
    void otherCurrenciesAreUnchanged() {
        assertEquals(d("0.61"), Money.round(d("0.605"), "EUR"));
        assertEquals("48,000.00 CZK", Money.format(d("48000"), "CZK"));
        assertEquals(List.of(d("33.34"), d("33.33"), d("33.33")), Money.allocate(d("100"), 3, "EUR"));
    }
}
