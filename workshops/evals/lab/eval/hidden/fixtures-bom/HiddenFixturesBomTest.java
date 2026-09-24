package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** Hidden acceptance tests for task fixtures-bom. The agent never sees this file. */
class HiddenFixturesBomTest {

    private static final String TEXT = "invoice_id,customer,net,tax_rate\nB-1,Müller GmbH,1.00,0.19\n";

    @Test
    void loadsTheLegacyExport() {
        List<Invoice> invoices = FixtureLoader.load(Path.of("data/legacy-export.csv"));
        assertEquals(3, invoices.size());
        assertEquals("L-2031", invoices.get(0).id());
        assertEquals("CZK", invoices.get(1).currency());
    }

    @Test
    void filesWithAndWithoutABomLoadTheSame(@TempDir Path dir) throws IOException {
        byte[] body = TEXT.getBytes(StandardCharsets.UTF_8);
        byte[] withBom = new byte[body.length + 3];
        withBom[0] = (byte) 0xEF;
        withBom[1] = (byte) 0xBB;
        withBom[2] = (byte) 0xBF;
        System.arraycopy(body, 0, withBom, 3, body.length);
        Path bom = Files.write(dir.resolve("bom.csv"), withBom);
        Path plain = Files.write(dir.resolve("plain.csv"), body);
        for (Path file : List.of(bom, plain)) {
            List<Invoice> invoices = FixtureLoader.load(file);
            assertEquals(1, invoices.size(), file.toString());
            assertEquals("B-1", invoices.get(0).id());
            assertEquals(new java.math.BigDecimal("1.00"), invoices.get(0).net());
        }
    }
}
