package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

class CliTest {

    private record Result(int code, String out, String err) {
    }

    private static Result run(String... args) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayOutputStream err = new ByteArrayOutputStream();
        int code = Cli.run(args, new PrintStream(out, true, StandardCharsets.UTF_8),
                new PrintStream(err, true, StandardCharsets.UTF_8));
        return new Result(code, out.toString(StandardCharsets.UTF_8), err.toString(StandardCharsets.UTF_8));
    }

    @Test
    void reportPrintsTotals() {
        Result result = run("report", "data/invoices.csv", "--currency", "usd");
        assertEquals(0, result.code());
        assertTrue(result.out().contains("Acme Corp"), result.out());
        assertTrue(result.out().contains("Total USD"), result.out());
    }

    @Test
    void exportPrintsCsv() {
        Result result = run("export", "data/invoices.csv");
        assertEquals(0, result.code());
        assertTrue(result.out().startsWith("invoice_id,customer,net,tax_rate,gross\nINV-001,\"North, Ltd\",100.00,0.21,121.00\n"),
                result.out());
    }

    @Test
    void duePrintsDueDatesAndOverdueFlags() {
        Result result = run("due", "data/invoices.csv", "--today", "2026-09-24");
        assertEquals(0, result.code());
        assertTrue(result.out().contains("INV-001  2026-10-01\n"), result.out());
        assertTrue(result.out().contains("INV-004  2026-09-14  OVERDUE\n"), result.out());
    }

    @Test
    void usageErrorsExitWithTwo() {
        assertEquals(2, run("report").code());
        assertEquals(2, run("frobnicate", "data/invoices.csv").code());
    }

    @Test
    void missingFileIsAnError() {
        Result result = run("report", "data/nope.csv");
        assertEquals(2, result.code());
        assertTrue(result.err().startsWith("error:"), result.err());
    }
}
