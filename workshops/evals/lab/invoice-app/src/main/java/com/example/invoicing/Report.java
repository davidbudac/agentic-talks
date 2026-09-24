package com.example.invoicing;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

/**
 * A small plain-text report: totals per customer and currency.
 *
 * <p>Amounts in different currencies are never added together; each customer gets one line
 * per currency. The table is meant for a terminal, so long customer names are shortened with
 * {@link CustomerNames#displayName(String, int)}.
 */
public final class Report {

    static final int NAME_WIDTH = 24;

    private Report() {
    }

    /** One report line: a customer's totals in one currency. */
    public record Entry(String customerName, String currency, int invoices, BigDecimal net, BigDecimal gross) {

        Entry add(Invoice invoice) {
            return new Entry(customerName, currency, invoices + 1, net.add(invoice.net()), gross.add(invoice.gross()));
        }
    }

    /**
     * Aggregates invoices into one entry per (customer, currency). Customers are grouped by
     * their normalised name, so "Müller GmbH" written with a decomposed umlaut lands on the
     * same line. If {@code currency} is not null, other currencies are left out.
     */
    public static List<Entry> summarise(List<Invoice> invoices, String currency) {
        String wanted = currency == null ? null : currency.strip().toUpperCase(Locale.ROOT);
        Map<List<String>, Entry> totals = new LinkedHashMap<>();
        for (Invoice invoice : invoices) {
            if (wanted != null && !invoice.currency().equals(wanted)) {
                continue;
            }
            String customer = CustomerNames.normalise(invoice.customer());
            List<String> key = List.of(customer, invoice.currency());
            Entry entry = totals.getOrDefault(key,
                    new Entry(customer, invoice.currency(), 0, BigDecimal.ZERO, BigDecimal.ZERO));
            totals.put(key, entry.add(invoice));
        }
        List<Entry> entries = new ArrayList<>(totals.values());
        entries.sort(Comparator.comparing(Entry::customerName).thenComparing(Entry::currency));
        return entries;
    }

    /** All currencies. */
    public static List<Entry> summarise(List<Invoice> invoices) {
        return summarise(invoices, null);
    }

    /** Gross total per currency across all customers, ordered by currency code. */
    public static Map<String, BigDecimal> grandTotals(List<Entry> entries) {
        Map<String, BigDecimal> result = new TreeMap<>();
        for (Entry entry : entries) {
            result.merge(entry.currency(), entry.gross(), BigDecimal::add);
        }
        return result;
    }

    /** Fixed-width text table with a totals footer. */
    public static String render(List<Entry> entries) {
        String header = String.format(Locale.ROOT, "%-" + NAME_WIDTH + "s  %3s  %16s  %16s",
                "Customer", "#", "Net", "Gross");
        String rule = "-".repeat(header.length());
        StringBuilder out = new StringBuilder().append(header).append('\n').append(rule).append('\n');
        for (Entry entry : entries) {
            out.append(String.format(Locale.ROOT, "%s  %3d  %16s  %16s\n",
                    pad(CustomerNames.displayName(entry.customerName(), NAME_WIDTH)), entry.invoices(),
                    Money.format(entry.net(), entry.currency()), Money.format(entry.gross(), entry.currency())));
        }
        out.append(rule).append('\n');
        grandTotals(entries).forEach((code, amount) -> out.append(String.format(Locale.ROOT,
                "%-" + NAME_WIDTH + "s  %3s  %16s  %16s\n", "Total " + code, "", "", Money.format(amount, code))));
        return out.toString();
    }

    /** Summarise and render in one call; what the CLI prints. */
    public static String build(List<Invoice> invoices, String currency) {
        return render(summarise(invoices, currency));
    }

    /** Pads to the name column, counting user-perceived characters rather than chars. */
    private static String pad(String name) {
        int length = name.codePointCount(0, name.length());
        return name + " ".repeat(Math.max(0, NAME_WIDTH - length));
    }
}
