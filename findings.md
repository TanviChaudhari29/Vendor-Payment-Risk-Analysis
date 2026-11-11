
# Vendor Payment Risk & Anomaly Analysis

## Dataset Overview
- Source: San Francisco Government — Vendor Payments (Vouchers)
- Fiscal Year: 2025
- Total Records: 515,694
- Total Columns: 32

## Initial Data Quality Findings

| Field | Missing Records | Missing Percentage |
|---|---:|---:|
| Supplier & Other Non-Supplier Payees | 0 | 0.00% |
| Purchase Order | 0 | 0.00% |
| Voucher | 0 | 0.00% |
| Contract Number | 257,870 | 50.00% |

## Key Observations
1. All records contain supplier, purchase order, and voucher references.
2. Exactly 257,870 records have blank contract numbers, representing approximately 50% of the dataset.
3. Missing contract numbers are a data-quality indicator, not evidence of fraud or an invalid payment.
4. Further analysis is needed to understand whether missing contract references vary by department, supplier, or purchasing category.

## Next Steps
- Validate financial amount fields.
- Analyze supplier payment concentration.
- Investigate repeated voucher references without assuming duplicate payments.
- Build SQL queries and a Power BI dashboard.
  
## Financial Amount Validation

- All three voucher amount columns contain valid numeric values.
- Vouchers Paid: 4,439 negative values (0.86%).
- Vouchers Pending: 7 negative values.
- Vouchers Pending Retainage: 0 negative values.
- Negative amounts require investigation and may represent accounting adjustments, refunds, or reversals.
- Negative values are not automatically evidence of fraud or incorrect payments.


