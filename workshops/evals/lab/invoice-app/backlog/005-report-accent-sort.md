# 005 · Sort the report like a person would

**Requested by:** account managers · **Size:** small

The report lists customers in raw code-point order, so `Čapek & syn s.r.o.`
and `Élodie Durand` appear after `Zeta Analytics`, and `Ábel` comes after
`Acme`. Nobody reads a customer list that way.

## Acceptance criteria

- `Report.summarise(...)` orders entries by customer using
  `CustomerNames.comparator()` (accent- and case-insensitive), then by
  currency code for the same customer.
- For `data/invoices.csv`, `Čapek & syn s.r.o.` comes before `Zeta Analytics`
  and `Élodie Durand` before `Müller GmbH`.
- The rendered table (`Report.build`) follows the same order.
- Grouping, totals and the currency filter are unchanged.
- Tests cover it; `./mvnw -q test` passes.

## Notes

`CustomerNames.comparator()` already exists; the report does not use it.
Likely files: `Report.java`, `ReportTest.java`.
