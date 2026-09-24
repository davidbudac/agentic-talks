package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

class InvoicesTest {

    private static BigDecimal d(String value) {
        return new BigDecimal(value);
    }

    @Test
    void grossAppliesTheRateAndRoundsOnce() {
        assertEquals(d("121.00"), Invoices.gross(d("100.00"), d("0.21"), "EUR"));
        assertEquals(d("0.61"), Invoices.gross(d("0.50"), d("0.21"), "EUR"));
        assertEquals(d("108.24"), Invoices.gross(d("99.99"), d("0.0825"), "USD"));
    }

    @Test
    void zeroRateKeepsTheNet() {
        assertEquals(d("100.00"), Invoices.gross(d("100"), BigDecimal.ZERO, "EUR"));
    }

    @Test
    void negativeRateIsRejected() {
        assertThrows(MoneyException.class, () -> Invoices.gross(d("1"), d("-0.1"), "EUR"));
    }

    @Test
    void totalsReconcile() {
        Invoices.Totals totals = Invoices.totals(
                List.of(new Invoices.Line(d("3"), d("0.335")), new Invoices.Line(d("1"), d("10"))), d("0.21"), "eur");
        assertEquals(d("11.01"), totals.net());
        assertEquals(d("13.32"), totals.gross());
        assertEquals(totals.gross(), totals.net().add(totals.tax()));
        assertEquals("EUR", totals.currency());
    }

    @Test
    void lineQuantityMustBePositive() {
        assertThrows(MoneyException.class, () -> new Invoices.Line(BigDecimal.ZERO, d("1")));
    }

    @Test
    void invoiceRecordNormalisesAndComputesGross() {
        Invoice invoice = Invoice.of("A-1", "North, Ltd", "100.00", "0.21", "eur");
        assertEquals("EUR", invoice.currency());
        assertEquals("net 30", invoice.terms());
        assertEquals(d("121.00"), invoice.gross());
    }

    @Test
    void invoiceWithoutCurrencyIsEur() {
        assertEquals("EUR", Invoice.of("A-2", "Acme", "1", "0", null).currency());
    }
}
