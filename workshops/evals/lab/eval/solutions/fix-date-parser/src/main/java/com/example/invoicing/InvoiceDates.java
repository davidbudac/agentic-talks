package com.example.invoicing;

import java.time.DateTimeException;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Issue dates and payment terms.
 *
 * <p>Fixture files use ISO dates ({@code 2026-09-24}). Older exports from the accounting tool
 * use the European dotted form ({@code 24.09.2026}). Payment terms are short phrases such as
 * {@code "net 30"}, {@code "end of month"} or {@code "on receipt"}.
 */
public final class InvoiceDates {

    private static final Pattern ISO = Pattern.compile("(\\d{4})-(\\d{2})-(\\d{2})");
    private static final Pattern DOTTED = Pattern.compile("(\\d{1,2})\\.(\\d{1,2})\\.(\\d{4})");
    private static final Pattern NET = Pattern.compile("net\\s+(\\d{1,3})");

    private InvoiceDates() {
    }

    /**
     * Parses an ISO date or a dotted date from the old exports.
     *
     * @throws IllegalArgumentException for anything that is not a valid date in one of the two forms
     */
    public static LocalDate parse(String text) {
        String value = text == null ? "" : text.strip();
        try {
            Matcher iso = ISO.matcher(value);
            if (iso.matches()) {
                return LocalDate.of(Integer.parseInt(iso.group(1)), Integer.parseInt(iso.group(2)),
                        Integer.parseInt(iso.group(3)));
            }
            Matcher dotted = DOTTED.matcher(value);
            if (dotted.matches()) {
                // The old exports are European: dotted dates are always day-first.
                int day = Integer.parseInt(dotted.group(1));
                int month = Integer.parseInt(dotted.group(2));
                return LocalDate.of(Integer.parseInt(dotted.group(3)), month, day);
            }
        } catch (DateTimeException e) {
            throw new IllegalArgumentException("invalid date: '" + text + "'", e);
        }
        throw new IllegalArgumentException("unrecognised date: '" + text + "'");
    }

    /** Last calendar day of the month that contains {@code day}. */
    public static LocalDate endOfMonth(LocalDate day) {
        return YearMonth.from(day).atEndOfMonth();
    }

    /**
     * Due date for an invoice issued on {@code issued} under {@code terms}: {@code "net N"}
     * (N days after issue), {@code "end of month"} or {@code "on receipt"}.
     */
    public static LocalDate dueDate(LocalDate issued, String terms) {
        String phrase = (terms == null ? Invoice.DEFAULT_TERMS : terms).strip()
                .toLowerCase(Locale.ROOT).replaceAll("\\s+", " ");
        if (phrase.equals("on receipt")) {
            return issued;
        }
        if (phrase.equals("end of month")) {
            return endOfMonth(issued);
        }
        Matcher net = NET.matcher(phrase);
        if (net.matches()) {
            return issued.plusDays(Integer.parseInt(net.group(1)));
        }
        throw new IllegalArgumentException("unknown payment terms: '" + terms + "'");
    }

    /** True if the invoice is past its due date on {@code today}. */
    public static boolean isOverdue(LocalDate issued, String terms, LocalDate today) {
        return today.isAfter(dueDate(issued, terms));
    }
}
