package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class CsvExportTest {

    @Test
    void writesTheHeaderForEmptyInput() {
        assertEquals("invoice_id,customer,net,tax_rate,gross\n", CsvExport.export(List.of()));
    }

    @Test
    void writesOneLinePerInvoiceInInputOrder() {
        String csv = CsvExport.export(List.of(
                Invoice.of("B-2", "Acme Corp", "99.99", "0.0825", "USD"),
                Invoice.of("A-1", "Zeta", "100.00", "0.21", "EUR")));
        assertEquals("""
                invoice_id,customer,net,tax_rate,gross
                B-2,Acme Corp,99.99,0.0825,108.24
                A-1,Zeta,100.00,0.21,121.00
                """, csv);
    }

    @Test
    void quotesCommasQuotesAndNewlines() {
        String csv = CsvExport.export(List.of(
                Invoice.of("A-1", "North, Ltd", "1", "0", "EUR"),
                Invoice.of("A-2", "Studio \"A\"", "1", "0", "EUR"),
                Invoice.of("A-3", "Line\nbreak", "1", "0", "EUR")));
        List<List<String>> rows = CsvReader.read(csv);
        assertEquals(List.of("North, Ltd", "Studio \"A\"", "Line\nbreak"),
                rows.subList(1, 4).stream().map(row -> row.get(1)).toList());
    }

    @Test
    void roundTripsTheFixtureCustomers() {
        List<Invoice> invoices = FixtureLoader.parseText("""
                invoice_id,customer,net,tax_rate
                X-1,Žluťoučký kůň a.s.,12500.00,0.21
                """);
        assertEquals(invoices.get(0).customerName(), CsvReader.read(CsvExport.export(invoices)).get(1).get(1));
    }
}
