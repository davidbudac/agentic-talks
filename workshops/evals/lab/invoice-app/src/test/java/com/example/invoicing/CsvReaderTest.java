package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

class CsvReaderTest {

    @Test
    void readsSimpleRecords() {
        assertEquals(List.of(List.of("a", "b"), List.of("1", "2")), CsvReader.read("a,b\n1,2\n"));
    }

    @Test
    void handlesQuotesCommasAndEmbeddedNewlines() {
        assertEquals(List.of(List.of("North, Ltd", "Studio \"A\"", "Line\nbreak")),
                CsvReader.read("\"North, Ltd\",\"Studio \"\"A\"\"\",\"Line\nbreak\"\n"));
    }

    @Test
    void acceptsCrlfAndMissingFinalNewline() {
        assertEquals(List.of(List.of("a", "b"), List.of("1", "")), CsvReader.read("a,b\r\n1,"));
    }

    @Test
    void skipsBlankLines() {
        assertEquals(List.of(List.of("a"), List.of("b")), CsvReader.read("a\n\nb\n"));
    }

    @Test
    void rejectsUnterminatedQuotes() {
        assertThrows(IllegalArgumentException.class, () -> CsvReader.read("\"open,1\n"));
    }
}
