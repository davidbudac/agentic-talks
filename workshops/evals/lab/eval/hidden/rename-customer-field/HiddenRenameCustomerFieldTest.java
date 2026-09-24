package com.example.invoicing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.lang.reflect.RecordComponent;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;

/** Hidden acceptance tests for task rename-customer-field. The agent never sees this file. */
class HiddenRenameCustomerFieldTest {

    @Test
    void theRecordComponentIsRenamed() {
        assertEquals(List.of("id", "customerName", "net", "taxRate", "currency", "issueDate", "terms"),
                Arrays.stream(Invoice.class.getRecordComponents()).map(RecordComponent::getName).toList());
    }

    @Test
    void noAliasAccessorIsLeft() {
        assertThrows(NoSuchMethodException.class, () -> Invoice.class.getMethod("customer"));
    }

    @Test
    void noCallerUsesTheOldAccessor() throws IOException {
        Pattern old = Pattern.compile("\\." + "customer" + "\\(\\)");
        List<String> hits;
        try (Stream<Path> files = Stream.concat(Files.walk(Path.of("src/main/java")), Files.walk(Path.of("src/test/java")))) {
            hits = files.filter(p -> p.toString().endsWith(".java")).filter(p -> {
                try {
                    return old.matcher(Files.readString(p)).find();
                } catch (IOException e) {
                    throw new java.io.UncheckedIOException(e);
                }
            }).map(Path::toString).toList();
        }
        assertEquals(List.of(), hits);
    }

    @Test
    void behaviourAndTheCsvContractAreUnchanged() {
        Invoice invoice = Invoice.of("A-1", "North, Ltd", "100.00", "0.21", "EUR");
        assertEquals("North, Ltd", invoice.customerName());
        assertTrue(CsvExport.export(List.of()).startsWith("invoice_id,customer,net,tax_rate,gross"));
        assertEquals("North, Ltd", Report.summarise(List.of(invoice)).get(0).customerName());
    }
}
