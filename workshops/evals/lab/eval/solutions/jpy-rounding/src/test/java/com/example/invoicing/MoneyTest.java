package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

class MoneyTest {

    @Test
    void parsesPlainAndSeparatedAmounts() {
        assertEquals(new BigDecimal("1000.50"), Money.parse(" 1_000.50 "));
        assertEquals(new BigDecimal("0.1"), Money.parse("0.1"));
    }

    @Test
    void rejectsEmptyAndNonNumbers() {
        assertThrows(MoneyException.class, () -> Money.parse(""));
        assertThrows(MoneyException.class, () -> Money.parse("12,50"));
        assertThrows(MoneyException.class, () -> Money.parse("NaN"));
    }

    @Test
    void roundsHalfUpToTheMinorUnit() {
        assertEquals(new BigDecimal("0.61"), Money.round(new BigDecimal("0.605"), "EUR"));
        assertEquals(new BigDecimal("0.60"), Money.round(new BigDecimal("0.6049"), "EUR"));
        assertEquals(new BigDecimal("-0.61"), Money.round(new BigDecimal("-0.605"), "USD"));
    }

    @Test
    void normalisesCurrencyCodes() {
        assertEquals("CZK", Money.normaliseCurrency(" czk "));
        assertEquals("EUR", Money.normaliseCurrency(null));
        assertThrows(MoneyException.class, () -> Money.normaliseCurrency("XYZ"));
    }

    @Test
    void quantumFollowsTheExponent() {
        assertEquals(new BigDecimal("0.01"), Money.quantum("GBP"));
    }

    @Test
    void formatsWithGroupingAndCode() {
        assertEquals("1,234.50 EUR", Money.format(new BigDecimal("1234.5"), "EUR"));
        assertEquals("48,000.00 CZK", Money.format(new BigDecimal("48000"), "czk"));
    }

    @Test
    void allocatesWithoutLosingACent() {
        assertEquals(List.of(new BigDecimal("33.34"), new BigDecimal("33.33"), new BigDecimal("33.33")),
                Money.allocate(new BigDecimal("100"), 3, "EUR"));
        assertEquals(new BigDecimal("100.00"),
                Money.allocate(new BigDecimal("100"), 7, "EUR").stream().reduce(BigDecimal.ZERO, BigDecimal::add));
    }

    @Test
    void yenHasNoMinorUnit() {
        assertEquals(new BigDecimal("1235"), Money.round(new BigDecimal("1234.5"), "JPY"));
        assertEquals("1,235 JPY", Money.format(new BigDecimal("1234.5"), "jpy"));
        assertEquals(List.of(new BigDecimal("34"), new BigDecimal("33"), new BigDecimal("33")),
                Money.allocate(new BigDecimal("100"), 3, "JPY"));
    }

    @Test
    void allocateNeedsAtLeastOnePart() {
        assertThrows(MoneyException.class, () -> Money.allocate(BigDecimal.TEN, 0, "EUR"));
    }
}
