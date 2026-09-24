package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import org.junit.jupiter.api.Test;

/**
 * A property check without a library: 300 random invoices from a fixed seed (so a
 * failure is reproducible), exported and read back. For every row: six cells, the
 * input order, the customer unchanged, the gross by the calculation rule, and the
 * currency upper-cased with EUR as the default.
 */
class CurrencyColumnPropertyTest {

    private static final String[] CUSTOMERS = {"Acme Corp", "North, Ltd", "Studio \"A\"", "Line\nbreak",
            "Čapek & syn s.r.o.", "Élodie Durand", "Østfold Fisk AS", "  spaced  "};
    private static final String[] CURRENCIES = {"EUR", "eur", "USD", "gbp", "CZK", "czk", null, ""};

    @Test
    void everyRowRoundTrips() {
        Random random = new Random(20260924L);
        List<Invoice> invoices = new ArrayList<>();
        List<String> inputCurrencies = new ArrayList<>();
        for (int i = 0; i < 300; i++) {
            String net = BigDecimal.valueOf(random.nextInt(10_000_000), random.nextInt(4)).toPlainString();
            String rate = BigDecimal.valueOf(random.nextInt(30), 2).toPlainString();
            String currency = CURRENCIES[random.nextInt(CURRENCIES.length)];
            inputCurrencies.add(currency);
            invoices.add(new Invoice("P-" + i, CUSTOMERS[random.nextInt(CUSTOMERS.length)],
                    new BigDecimal(net), new BigDecimal(rate), currency, null, null));
        }
        List<List<String>> rows = CsvReader.read(CsvExport.export(invoices));
        assertEquals(invoices.size() + 1, rows.size());
        for (int i = 0; i < invoices.size(); i++) {
            Invoice invoice = invoices.get(i);
            List<String> row = rows.get(i + 1);
            assertEquals(6, row.size(), row.toString());
            assertEquals(invoice.id(), row.get(0));
            assertEquals(invoice.customer(), row.get(1));
            assertEquals(invoice.gross().toPlainString(), row.get(4), row.toString());
            String input = inputCurrencies.get(i);
            String expected = input == null || input.isBlank() ? "EUR" : input.toUpperCase(Locale.ROOT);
            assertEquals(expected, row.get(5), row.toString());
        }
    }
}
