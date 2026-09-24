package com.example.invoicing;

import java.util.List;
import java.util.stream.Collectors;

/**
 * CSV export: the feature talk 03 builds against an acceptance contract.
 *
 * <p>Contract: keep the calculation rule, write the five named columns, quote commas, quotes
 * and line breaks, keep the input order and write the header for empty input. No file or
 * network side effects: the caller decides where the text goes.
 */
public final class CsvExport {

    public static final List<String> COLUMNS = List.of("invoice_id", "customer", "net", "tax_rate", "gross");

    private CsvExport() {
    }

    /** Returns the CSV text with a header line, also when {@code invoices} is empty. */
    public static String export(List<Invoice> invoices) {
        StringBuilder out = new StringBuilder();
        writeLine(out, COLUMNS);
        for (Invoice invoice : invoices) {
            writeLine(out, List.of(
                    invoice.id(),
                    invoice.customer(),
                    invoice.net().toPlainString(),
                    invoice.taxRate().toPlainString(),
                    invoice.gross().toPlainString()));
        }
        return out.toString();
    }

    private static void writeLine(StringBuilder out, List<String> cells) {
        out.append(cells.stream().map(CsvExport::quote).collect(Collectors.joining(","))).append('\n');
    }

    static String quote(String cell) {
        if (cell.contains(",") || cell.contains("\"") || cell.contains("\n") || cell.contains("\r")) {
            return '"' + cell.replace("\"", "\"\"") + '"';
        }
        return cell;
    }
}
