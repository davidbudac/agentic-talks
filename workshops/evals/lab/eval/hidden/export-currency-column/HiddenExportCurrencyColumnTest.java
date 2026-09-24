package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Hidden acceptance tests for task export-currency-column. The agent never sees this file. */
class HiddenExportCurrencyColumnTest {

    private static final List<Invoice> INVOICES = List.of(
            Invoice.of("A-1", "North, Ltd", "100.00", "0.21", "eur"),
            Invoice.of("A-2", "Line\nbreak", "0.50", "0.21", "CZK"),
            new Invoice("A-3", "No currency", new BigDecimal("10"), BigDecimal.ZERO, null, null, null));

    @Test
    void headerHasTheCurrencyColumnLast() {
        assertEquals(List.of(List.of("invoice_id", "customer", "net", "tax_rate", "gross", "currency")),
                CsvReader.read(CsvExport.export(List.of())));
    }

    @Test
    void valuesAreUpperCaseWithEurAsTheDefault() {
        List<List<String>> rows = CsvReader.read(CsvExport.export(INVOICES)).subList(1, 4);
        assertEquals(List.of("EUR", "CZK", "EUR"), rows.stream().map(r -> r.get(5)).toList());
        assertEquals(List.of("121.00", "0.61", "10.00"), rows.stream().map(r -> r.get(4)).toList());
        assertEquals(List.of("A-1", "A-2", "A-3"), rows.stream().map(r -> r.get(0)).toList());
        assertEquals("Line\nbreak", rows.get(1).get(1));
        rows.forEach(r -> assertEquals(6, r.size(), r.toString()));
    }
}
