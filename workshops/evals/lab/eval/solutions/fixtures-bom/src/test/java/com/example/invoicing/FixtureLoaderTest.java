package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.Test;

class FixtureLoaderTest {

    @Test
    void loadsTheMainFixture() {
        List<Invoice> invoices = FixtureLoader.load(Path.of("data/invoices.csv"));
        assertEquals(12, invoices.size());
        assertEquals("INV-001", invoices.get(0).id());
        assertEquals("Line\nbreak", invoices.get(2).customer());
        assertEquals(LocalDate.of(2026, 8, 15), invoices.get(3).issueDate());
        assertEquals(new BigDecimal("0.0825"), invoices.get(11).taxRate());
    }

    @Test
    void appliesDefaultsForOptionalColumns() {
        Invoice invoice = FixtureLoader.parseText("invoice_id,customer,net,tax_rate\nB-1,Acme,10,0.2\n").get(0);
        assertEquals("EUR", invoice.currency());
        assertEquals("net 30", invoice.terms());
        assertNull(invoice.issueDate());
    }

    @Test
    void reportsMissingColumns() {
        FixtureException e = assertThrows(FixtureException.class,
                () -> FixtureLoader.parseText("invoice_id,customer,net\nB-1,Acme,10\n"));
        assertTrue(e.getMessage().contains("tax_rate"), e.getMessage());
    }

    @Test
    void reportsDuplicateIdsWithTheRow() {
        FixtureException e = assertThrows(FixtureException.class, () -> FixtureLoader.parseText(
                "invoice_id,customer,net,tax_rate\nB-1,A,1,0\nB-1,B,2,0\n"));
        assertEquals("row 3: duplicate invoice_id B-1", e.getMessage());
    }

    @Test
    void reportsBadAmountsAndCurrencies() {
        assertThrows(FixtureException.class, () -> FixtureLoader.parseText(
                "invoice_id,customer,net,tax_rate\nB-1,A,ten,0\n"));
        assertThrows(FixtureException.class, () -> FixtureLoader.parseText(
                "invoice_id,customer,net,tax_rate,currency\nB-1,A,1,0,XYZ\n"));
    }

    @Test
    void readsFilesWithAByteOrderMark() {
        List<Invoice> invoices = FixtureLoader.load(Path.of("data/legacy-export.csv"));
        assertEquals("L-2031", invoices.get(0).id());
        assertEquals(1, FixtureLoader.parseText("\uFEFFinvoice_id,customer,net,tax_rate\nB-1,A,1,0\n").size());
    }

    @Test
    void rejectsEmptyIds() {
        assertThrows(FixtureException.class, () -> FixtureLoader.parseText(
                "invoice_id,customer,net,tax_rate\n ,A,1,0\n"));
    }
}
