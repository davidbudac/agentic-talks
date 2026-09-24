package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class CustomerNamesTest {

    @Test
    void normaliseComposesAndCollapsesWhitespace() {
        assertEquals("Müller GmbH", CustomerNames.normalise("  Müller   GmbH "));
    }

    @Test
    void normaliseRejectsNull() {
        assertThrows(IllegalArgumentException.class, () -> CustomerNames.normalise(null));
    }

    @Test
    void stripAccentsRemovesCombiningMarks() {
        assertEquals("Capek", CustomerNames.stripAccents("Čapek"));
        assertEquals("Zlutoucky kun", CustomerNames.stripAccents("Žluťoučký kůň"));
    }

    @Test
    void comparatorIgnoresCaseAndAccents() {
        List<String> names = new ArrayList<>(List.of("zeta", "Čapek", "Alpha", "capek"));
        names.sort(CustomerNames.comparator());
        assertEquals(List.of("Alpha", "capek", "Čapek", "zeta"), names);
    }

    @Test
    void matchesIgnoresCaseAndAccents() {
        assertTrue(CustomerNames.matches("Müller GmbH", "muller"));
        assertTrue(CustomerNames.matches("Čapek & syn s.r.o.", "CAPEK"));
        assertFalse(CustomerNames.matches("Acme Corp", "capek"));
    }

    @Test
    void initialsKeepAccents() {
        assertEquals("ÉD", CustomerNames.initials("Élodie Durand"));
        assertEquals("AC", CustomerNames.initials("acme corp inc"));
    }

    @Test
    void displayNameKeepsShortNames() {
        assertEquals("Acme Corp", CustomerNames.displayName("Acme Corp", 24));
    }

    @Test
    void displayNameCutsWithEllipsisAndReplacesNewlines() {
        assertEquals("Line b…", CustomerNames.displayName("Line\nbreak", 7));
    }

    @Test
    void displayNameNeverSplitsAnAccent() {
        String cut = CustomerNames.displayName("Žlučký kůn", 4);
        assertEquals("Žlu…", java.text.Normalizer.normalize(cut, java.text.Normalizer.Form.NFC));
    }
}
