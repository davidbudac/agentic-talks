package com.example.invoicing;

import java.math.BigDecimal;
import java.util.List;

/**
 * Invoice calculation. The rule from talk 02 still holds: apply the rate to the exact net
 * amount and round once, half up, at the end.
 */
public final class Invoices {

    private Invoices() {
    }

    /** One invoice line: quantity times unit price. */
    public record Line(BigDecimal quantity, BigDecimal unitPrice) {

        public Line {
            if (quantity.signum() <= 0) {
                throw new MoneyException("quantity must be positive: " + quantity);
            }
        }

        /** Unrounded net amount of the line. */
        public BigDecimal net() {
            return quantity.multiply(unitPrice);
        }
    }

    /** Totals that always reconcile: {@code net + tax == gross}. */
    public record Totals(BigDecimal net, BigDecimal tax, BigDecimal gross, String currency) {
    }

    /** Applies the supplied rate and rounds once, half up, to the minor unit. */
    public static BigDecimal gross(BigDecimal net, BigDecimal taxRate, String currency) {
        if (taxRate.signum() < 0) {
            throw new MoneyException("negative tax rate: " + taxRate);
        }
        return Money.round(net.multiply(BigDecimal.ONE.add(taxRate)), currency);
    }

    /**
     * Totals for a multi-line invoice. The net is summed exactly and each figure is rounded
     * once at the end, so the tax is {@code gross - net} and the three numbers reconcile.
     */
    public static Totals totals(List<Line> lines, BigDecimal taxRate, String currency) {
        BigDecimal exactNet = lines.stream().map(Line::net).reduce(BigDecimal.ZERO, BigDecimal::add);
        BigDecimal net = Money.round(exactNet, currency);
        BigDecimal gross = gross(exactNet, taxRate, currency);
        return new Totals(net, gross.subtract(net), gross, Money.normaliseCurrency(currency));
    }
}
