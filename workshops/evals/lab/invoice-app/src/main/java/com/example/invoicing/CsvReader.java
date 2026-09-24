package com.example.invoicing;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * A small RFC 4180 CSV reader: comma-separated, fields optionally quoted with {@code "},
 * {@code ""} for a literal quote, commas and line breaks allowed inside quotes, and CRLF or
 * LF line endings. Files are read as UTF-8.
 */
public final class CsvReader {

    private CsvReader() {
    }

    /** Reads every record of a UTF-8 file. */
    public static List<List<String>> read(Path path) {
        try (Reader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            return read(reader);
        } catch (IOException e) {
            throw new UncheckedIOException("cannot read " + path, e);
        }
    }

    /** Reads every record from a string. */
    public static List<List<String>> read(String text) {
        try {
            return read(new StringReader(text));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    /** Reads every record from a reader. Blank lines between records are skipped. */
    public static List<List<String>> read(Reader source) throws IOException {
        Reader reader = source.markSupported() ? source : new BufferedReader(source);
        List<List<String>> records = new ArrayList<>();
        List<String> record = new ArrayList<>();
        StringBuilder field = new StringBuilder();
        boolean quoted = false;
        boolean fieldStarted = false;
        int c;
        while ((c = reader.read()) != -1) {
            char ch = (char) c;
            if (quoted) {
                if (ch == '"') {
                    reader.mark(1);
                    int next = reader.read();
                    if (next == '"') {
                        field.append('"');
                    } else {
                        quoted = false;
                        if (next != -1) {
                            reader.reset();
                        }
                    }
                } else {
                    field.append(ch);
                }
                continue;
            }
            switch (ch) {
                case '"' -> {
                    quoted = true;
                    fieldStarted = true;
                }
                case ',' -> {
                    record.add(field.toString());
                    field.setLength(0);
                    fieldStarted = true;
                }
                case '\r' -> {
                    // part of a CRLF line ending; the '\n' ends the record
                }
                case '\n' -> {
                    endRecord(records, record, field, fieldStarted);
                    record = new ArrayList<>();
                    fieldStarted = false;
                }
                default -> {
                    field.append(ch);
                    fieldStarted = true;
                }
            }
        }
        if (quoted) {
            throw new IllegalArgumentException("unterminated quoted field at end of input");
        }
        endRecord(records, record, field, fieldStarted);
        return records;
    }

    private static void endRecord(List<List<String>> records, List<String> record, StringBuilder field,
                                  boolean fieldStarted) {
        if (!fieldStarted && record.isEmpty()) {
            return; // blank line
        }
        record.add(field.toString());
        field.setLength(0);
        records.add(record);
    }
}
