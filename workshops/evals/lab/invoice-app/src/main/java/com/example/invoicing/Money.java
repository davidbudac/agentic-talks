package com.example.invoicing;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Money helpers: parsing amounts, currency exponents and the one rounding rule.
 *
 * <p>Every amount is a {@link BigDecimal}. Doubles are never accepted: {@code 0.1 + 0.2}
 * is not {@code 0.3} in binary floating point, and invoices must add up.
 *
 * <p>Rounding happens once, at the end of a calculation, with {@link RoundingMode#HALF_UP}
 * to the currency's minor unit. Intermediate values keep full precision.
 */
public final class Money {

    /** Minor-unit exponents per ISO 4217 code. Example data, not a complete table. */
    static final Map<String, Integer> CURRENCY_EXPONENTS = Map.of(
            "EUR", 2,
            "USD", 2,
            "GBP", 2,
            "CZK", 2);

    public static final String DEFAULT_CURRENCY = "EUR";

    private Money() {
    }

    /**
     * Parses an amount. Surrounding spaces and {@code _} digit separators are fine
     * ({@code " 1_000.50 "}); anything else that is not a finite decimal is rejected.
     */
    public static BigDecimal parse(String text) {
        if (text == null || text.isBlank()) {
            throw new MoneyException("empty amount");
        }
        String cleaned = text.strip().replace("_", "");
        try {
            return new BigDecimal(cleaned);
        } catch (NumberFormatException e) {
            throw new MoneyException("not a number: '" + text + "'");
        }
    }

    /** Upper-case ISO code; {@code null} or blank means the default currency. */
    public static String normaliseCurrency(String currency) {
        String code = currency == null || currency.isBlank()
                ? DEFAULT_CURRENCY
                : currency.strip().toUpperCase(Locale.ROOT);
        if (!CURRENCY_EXPONENTS.containsKey(code)) {
            throw new MoneyException("unknown currency: '" + currency + "'");
        }
        return code;
    }

    /** Number of decimal places in the currency's minor unit. */
    public static int exponent(String currency) {
        return CURRENCY_EXPONENTS.get(normaliseCurrency(currency));
    }

    /** The smallest unit, e.g. {@code 0.01} for EUR. */
    public static BigDecimal quantum(String currency) {
        return BigDecimal.ONE.scaleByPowerOfTen(-exponent(currency));
    }

    /** Rounds once, half up, to the currency's minor unit. */
    public static BigDecimal round(BigDecimal amount, String currency) {
        return amount.setScale(exponent(currency), RoundingMode.HALF_UP);
    }

    /**
     * Formats for humans: thousands separators and the currency code,
     * e.g. {@code format(new BigDecimal("1234.5"), "EUR")} is {@code "1,234.50 EUR"}.
     */
    public static String format(BigDecimal amount, String currency) {
        String code = normaliseCurrency(currency);
        return String.format(Locale.ROOT, "%,.2f %s", round(amount, code), code);
    }

    /**
     * Splits {@code total} into {@code parts} amounts that add up exactly, using the
     * largest-remainder method: every part gets the floor share and the leftover minor
     * units go to the first parts. Useful for instalments.
     */
    public static List<BigDecimal> allocate(BigDecimal total, int parts, String currency) {
        if (parts < 1) {
            throw new MoneyException("parts must be at least 1");
        }
        BigInteger units = round(total, currency).movePointRight(2).toBigIntegerExact();
        BigInteger[] split = units.divideAndRemainder(BigInteger.valueOf(parts));
        int leftover = split[1].intValueExact();
        List<BigDecimal> shares = new ArrayList<>(parts);
        for (int i = 0; i < parts; i++) {
            BigInteger share = split[0].add(i < leftover ? BigInteger.ONE : BigInteger.ZERO);
            shares.add(new BigDecimal(share).movePointLeft(2));
        }
        return shares;
    }
}
