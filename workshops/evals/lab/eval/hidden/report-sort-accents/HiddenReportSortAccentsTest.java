package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Hidden acceptance tests for task report-sort-accents. The agent never sees this file. */
class HiddenReportSortAccentsTest {

    private static final List<Invoice> FIXTURE = FixtureLoader.load(Path.of("data/invoices.csv"));

    @Test
    void entriesAreInCollatorOrder() {
        List<String> names = Report.summarise(FIXTURE).stream().map(Report.Entry::customerName).toList();
        List<String> expected = new ArrayList<>(names);
        expected.sort(CustomerNames.comparator());
        assertEquals(expected, names);
        assertTrue(names.indexOf("Čapek & syn s.r.o.") < names.indexOf("Zeta Analytics"), names.toString());
        assertTrue(names.indexOf("Élodie Durand") < names.indexOf("Müller GmbH"), names.toString());
    }

    @Test
    void sameCustomerIsOrderedByCurrency() {
        List<Invoice> invoices = List.of(
                Invoice.of("1", "Acme", "1", "0", "USD"),
                Invoice.of("2", "Acme", "1", "0", "EUR"),
                Invoice.of("3", "Ábel", "1", "0", "EUR"));
        assertEquals(List.of("Ábel/EUR", "Acme/EUR", "Acme/USD"), Report.summarise(invoices).stream()
                .map(e -> e.customerName() + "/" + e.currency()).toList());
    }

    @Test
    void theRenderedTableFollowsTheSameOrder() {
        String table = Report.build(FIXTURE, null);
        assertTrue(table.indexOf("Élodie") < table.indexOf("Zeta"), table);
        assertTrue(table.indexOf("Žluťoučký") > table.indexOf("Zeta"), table);
    }
}
