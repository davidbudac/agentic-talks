package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ReportTest {

    private static final List<Invoice> FIXTURE = FixtureLoader.load(Path.of("data/invoices.csv"));

    @Test
    void groupsByNormalisedCustomerAndCurrency() {
        List<Invoice> invoices = List.of(
                Invoice.of("1", "Müller GmbH", "10", "0", "EUR"),
                Invoice.of("2", "Müller  GmbH", "5", "0", "EUR"),
                Invoice.of("3", "Müller GmbH", "7", "0", "USD"));
        List<Report.Entry> entries = Report.summarise(invoices);
        assertEquals(2, entries.size());
        assertEquals(2, entries.get(0).invoices());
        assertEquals(new BigDecimal("15"), entries.get(0).net());
        assertEquals("Müller GmbH", entries.get(0).customerName());
    }

    @Test
    void ordersPlainNamesAlphabeticallyThenByCurrency() {
        List<Invoice> invoices = List.of(
                Invoice.of("1", "Beta", "1", "0", "USD"),
                Invoice.of("2", "Alpha", "1", "0", "EUR"),
                Invoice.of("3", "Beta", "1", "0", "EUR"));
        assertEquals(List.of("Alpha/EUR", "Beta/EUR", "Beta/USD"), Report.summarise(invoices).stream()
                .map(e -> e.customerName() + "/" + e.currency()).toList());
    }

    @Test
    void currencyFilterKeepsOnlyThatCurrency() {
        List<Report.Entry> entries = Report.summarise(FIXTURE, "czk");
        assertEquals(2, entries.size());
        assertTrue(entries.stream().allMatch(e -> e.currency().equals("CZK")));
    }

    @Test
    void grandTotalsNeverMixCurrencies() {
        Map<String, BigDecimal> totals = Report.grandTotals(Report.summarise(FIXTURE));
        assertEquals(List.of("CZK", "EUR", "GBP", "USD"), List.copyOf(totals.keySet()));
        assertEquals(new BigDecimal("73205.00"), totals.get("CZK"));
    }

    @Test
    void rendersATableWithTotals() {
        String table = Report.build(FIXTURE, "GBP");
        assertTrue(table.startsWith("Customer"), table);
        assertTrue(table.contains("Zeta Analytics"), table);
        assertTrue(table.contains("1,176.48 GBP"), table);
        assertTrue(table.contains("Total GBP"), table);
        assertFalse(table.contains("EUR"), table);
    }

    @Test
    void shortensLongNamesInTheTable() {
        String table = Report.build(List.of(Invoice.of("1", "A very long customer name indeed, Ltd", "1", "0", "EUR")), null);
        assertTrue(table.contains("A very long customer na…"), table);
    }
}
