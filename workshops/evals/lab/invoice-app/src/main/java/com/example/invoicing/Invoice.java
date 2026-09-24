package com.example.invoicing;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * One invoice as the fixtures describe it.
 *
 * <p>Tax rates are supplied by the caller ({@code 0.21} for 21 %). This package deliberately
 * has no tax table: rates depend on the country, the product and the date, and belong to
 * whoever issues the invoice.
 *
 * @param id        invoice number, unique within a fixture file
 * @param customer  customer name as written (see {@link CustomerNames} for comparing names)
 * @param net       net amount, exact (not rounded)
 * @param taxRate   tax rate as a fraction, never negative
 * @param currency  ISO 4217 code, normalised to upper case; {@code null} means EUR
 * @param issueDate issue date, or {@code null} when the fixture has none
 * @param terms     payment terms such as {@code "net 30"}; {@code null} means net 30
 */
public record Invoice(String id, String customer, BigDecimal net, BigDecimal taxRate,
                      String currency, LocalDate issueDate, String terms) {

    public static final String DEFAULT_TERMS = "net 30";

    public Invoice {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(customer, "customer");
        Objects.requireNonNull(net, "net");
        Objects.requireNonNull(taxRate, "taxRate");
        if (taxRate.signum() < 0) {
            throw new MoneyException("negative tax rate: " + taxRate);
        }
        currency = Money.normaliseCurrency(currency);
        terms = terms == null || terms.isBlank() ? DEFAULT_TERMS : terms;
    }

    /** Convenience for tests and examples: no issue date, net 30. */
    public static Invoice of(String id, String customer, String net, String taxRate, String currency) {
        return new Invoice(id, customer, Money.parse(net), Money.parse(taxRate), currency, null, null);
    }

    /** Gross amount: the rate applied to the exact net, rounded once. */
    public BigDecimal gross() {
        return Invoices.gross(net, taxRate, currency);
    }
}
