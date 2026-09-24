package com.example.invoicing;

import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Command-line entry point.
 *
 * <pre>
 *   report FILE [--currency CODE]   totals per customer and currency
 *   export FILE                     the five-column CSV from CsvExport
 *   due FILE [--today YYYY-MM-DD]   due date per invoice, marking overdue ones
 * </pre>
 */
public final class Cli {

    static final String USAGE = """
            usage: invoicing report FILE [--currency CODE]
                   invoicing export FILE
                   invoicing due FILE [--today YYYY-MM-DD]
            """;

    private Cli() {
    }

    public static void main(String[] args) {
        PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);
        PrintStream err = new PrintStream(System.err, true, StandardCharsets.UTF_8);
        System.exit(run(args, out, err));
    }

    /** Runs one command; returns the exit code (0 ok, 2 usage or input error). */
    public static int run(String[] args, PrintStream out, PrintStream err) {
        if (args.length < 2) {
            err.print(USAGE);
            return 2;
        }
        String command = args[0];
        Path file = Path.of(args[1]);
        List<String> rest = new ArrayList<>(List.of(args).subList(2, args.length));
        try {
            switch (command) {
                case "report" -> out.print(Report.build(FixtureLoader.load(file), option(rest, "--currency")));
                case "export" -> out.print(CsvExport.export(FixtureLoader.load(file)));
                case "due" -> {
                    String today = option(rest, "--today");
                    out.print(due(FixtureLoader.load(file), today == null ? null : InvoiceDates.parse(today)));
                }
                default -> {
                    err.print(USAGE);
                    return 2;
                }
            }
        } catch (RuntimeException e) {
            err.println("error: " + e.getMessage());
            return 2;
        }
        return 0;
    }

    static String due(List<Invoice> invoices, LocalDate today) {
        StringBuilder out = new StringBuilder();
        for (Invoice invoice : invoices) {
            if (invoice.issueDate() == null) {
                out.append(invoice.id()).append("  (no issue date)\n");
                continue;
            }
            LocalDate due = InvoiceDates.dueDate(invoice.issueDate(), invoice.terms());
            boolean overdue = today != null && InvoiceDates.isOverdue(invoice.issueDate(), invoice.terms(), today);
            out.append(invoice.id()).append("  ").append(due).append(overdue ? "  OVERDUE" : "").append('\n');
        }
        return out.toString();
    }

    private static String option(List<String> args, String name) {
        int index = args.indexOf(name);
        if (index < 0) {
            return null;
        }
        if (index + 1 >= args.size()) {
            throw new IllegalArgumentException(name + " needs a value");
        }
        return args.get(index + 1);
    }
}
