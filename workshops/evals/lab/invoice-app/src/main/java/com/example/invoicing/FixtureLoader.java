package com.example.invoicing;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Loads invoices from CSV fixtures.
 *
 * <p>Required columns: {@code invoice_id}, {@code customer}, {@code net} and {@code tax_rate}.
 * Optional columns: {@code currency} (default EUR), {@code issue_date} (ISO or dotted) and
 * {@code terms} (default net 30). Row numbers in errors count the header as row 1.
 */
public final class FixtureLoader {

    public static final List<String> REQUIRED_COLUMNS = List.of("invoice_id", "customer", "net", "tax_rate");

    private FixtureLoader() {
    }

    /** Loads a fixture file from disk. */
    public static List<Invoice> load(Path path) {
        return parse(CsvReader.read(path));
    }

    /** Parses fixture rows from CSV text; handy in tests. */
    public static List<Invoice> parseText(String text) {
        return parse(CsvReader.read(text));
    }

    /** Parses fixture rows from a reader. */
    public static List<Invoice> parse(Reader reader) {
        try {
            return parse(CsvReader.read(reader));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    static List<Invoice> parse(List<List<String>> records) {
        if (records.isEmpty()) {
            throw new FixtureException("empty file: no header");
        }
        Map<String, Integer> columns = new HashMap<>();
        List<String> header = records.get(0);
        for (int i = 0; i < header.size(); i++) {
            columns.putIfAbsent(header.get(i).strip(), i);
        }
        List<String> missing = REQUIRED_COLUMNS.stream().filter(c -> !columns.containsKey(c)).toList();
        if (!missing.isEmpty()) {
            throw new FixtureException("missing column(s): " + String.join(", ", missing));
        }
        List<Invoice> invoices = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        for (int index = 1; index < records.size(); index++) {
            int row = index + 1;
            List<String> record = records.get(index);
            String id = cell(record, columns, "invoice_id").strip();
            if (id.isEmpty()) {
                throw new FixtureException("row " + row + ": empty invoice_id");
            }
            if (!seen.add(id)) {
                throw new FixtureException("row " + row + ": duplicate invoice_id " + id);
            }
            try {
                String issued = cell(record, columns, "issue_date").strip();
                LocalDate issueDate = issued.isEmpty() ? null : InvoiceDates.parse(issued);
                invoices.add(new Invoice(id, cell(record, columns, "customer"),
                        Money.parse(cell(record, columns, "net")),
                        Money.parse(cell(record, columns, "tax_rate")),
                        cell(record, columns, "currency"), issueDate, cell(record, columns, "terms")));
            } catch (IllegalArgumentException e) {
                throw new FixtureException("row " + row + ": " + e.getMessage(), e);
            }
        }
        return invoices;
    }

    private static String cell(List<String> record, Map<String, Integer> columns, String name) {
        Integer index = columns.get(name);
        return index == null || index >= record.size() ? "" : record.get(index);
    }
}
