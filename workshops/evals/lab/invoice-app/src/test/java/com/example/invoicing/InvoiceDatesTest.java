package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;

class InvoiceDatesTest {

    @Test
    void parsesIsoDates() {
        assertEquals(LocalDate.of(2026, 9, 24), InvoiceDates.parse("2026-09-24"));
    }

    @Test
    void parsesUnambiguousDottedDates() {
        assertEquals(LocalDate.of(2026, 8, 28), InvoiceDates.parse("28.08.2026"));
        assertEquals(LocalDate.of(2026, 12, 31), InvoiceDates.parse(" 31.12.2026 "));
    }

    @Test
    void rejectsGarbageAndImpossibleDates() {
        assertThrows(IllegalArgumentException.class, () -> InvoiceDates.parse("next week"));
        assertThrows(IllegalArgumentException.class, () -> InvoiceDates.parse("2026-02-30"));
        assertThrows(IllegalArgumentException.class, () -> InvoiceDates.parse(""));
    }

    @Test
    void netTerms() {
        assertEquals(LocalDate.of(2026, 10, 1), InvoiceDates.dueDate(LocalDate.of(2026, 9, 1), "net 30"));
        assertEquals(LocalDate.of(2026, 9, 16), InvoiceDates.dueDate(LocalDate.of(2026, 9, 2), "Net  14"));
    }

    @Test
    void endOfMonthAndOnReceipt() {
        assertEquals(LocalDate.of(2028, 2, 29), InvoiceDates.dueDate(LocalDate.of(2028, 2, 3), "end of month"));
        assertEquals(LocalDate.of(2026, 9, 3), InvoiceDates.dueDate(LocalDate.of(2026, 9, 3), "on receipt"));
    }

    @Test
    void unknownTermsAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> InvoiceDates.dueDate(LocalDate.of(2026, 1, 1), "whenever"));
    }

    @Test
    void overdueIsStrictlyAfterTheDueDate() {
        LocalDate issued = LocalDate.of(2026, 9, 1);
        assertFalse(InvoiceDates.isOverdue(issued, "net 30", LocalDate.of(2026, 10, 1)));
        assertTrue(InvoiceDates.isOverdue(issued, "net 30", LocalDate.of(2026, 10, 2)));
    }
}
