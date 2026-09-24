package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * The weak checker for lab 3. It looks reasonable in a code review: the new column is
 * there. Find out how little it actually proves.
 */
class WeakCurrencyColumnTest {

    @Test
    void headerMentionsTheCurrency() {
        String csv = CsvExport.export(List.of());
        assertTrue(csv.contains("currency"), csv);
    }
}
