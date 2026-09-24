package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;

/** Hidden acceptance tests for task fix-date-parser. The agent never sees this file. */
class HiddenFixDateParserTest {

    @Test
    void dottedDatesAreDayFirst() {
        assertEquals(LocalDate.of(2026, 9, 5), InvoiceDates.parse("05.09.2026"));
        assertEquals(LocalDate.of(2027, 2, 1), InvoiceDates.parse("1.2.2027"));
    }

    @Test
    void unambiguousAndIsoDatesStillParse() {
        assertEquals(LocalDate.of(2026, 12, 31), InvoiceDates.parse("31.12.2026"));
        assertEquals(LocalDate.of(2026, 9, 24), InvoiceDates.parse("2026-09-24"));
    }

    @Test
    void monthFirstIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> InvoiceDates.parse("12.31.2026"));
    }

    @Test
    void dueDateFromADottedIssueDate() {
        assertEquals(LocalDate.of(2026, 10, 5), InvoiceDates.dueDate(InvoiceDates.parse("05.09.2026"), "net 30"));
    }
}
