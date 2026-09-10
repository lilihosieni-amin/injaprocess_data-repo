# Sandogh - Chalebagh

- spreadsheetId: `1XSoT0g0qz-ym70FFFtrs-kdJfFla5YGpQUl8gdpiEk0`
- url: https://docs.google.com/spreadsheets/d/1XSoT0g0qz-ym70FFFtrs-kdJfFla5YGpQUl8gdpiEk0/edit?usp=drivesdk
- locale: en_US | timezone: Asia/Tehran
- exported: 2026-08-29T09:27:35.540Z

## شیت‌ها

| # | نام | مخفی | ابعاد | فریز |
|---|---|---|---|---|
| 1 | ضایعات | - | 363×4 | 1/0 |
| 2 | تعداد فیش هرشب بجز سالن | - | 585×4 | 1/0 |
| 3 | OFF اجرایی | - | 372×4 | 1/0 |
| 4 | SheetsFileIds | **بله** | 2×2 | 1/0 |
| 5 | نیازمندیها و مشکلات | - | 359×3 | 1/0 |

## بازه‌های نام‌گذاری‌شده

- `SheetsFileId_Accounting_Chalebagh` → `SheetsFileIds!B2`

## فرمول‌های یکتا

### تعداد فیش هرشب بجز سالن

- `B2` ×398  →  `=LET(
  inputDate, A2,
  sheetName, "اهداف فروش",
  dataRange, "A:G",
  result,
    IF(
      ISBLANK(inputDate),
      "",
      LET(
        date, GREG_TO_JALALI(inputDate),
        monthName, GET_JALALI_MONTH_NAME(date),
        year, GET_JALALI_YEAR(date),
        data, IMPORT_FROM_SHEET(SheetsFileId_Accounting_Chalebagh, sheetName, dataRange),
        filteredData, FILTER(data, INDEX(data,,2) = monthName, INDEX(data,,3) = year),
        INDEX(filteredData,,5)
      )
    ),
  result
)
`
- `D2` ×399  →  `=C2-B2`

> اسکن فقط تا ردیف 400.


## توابع استفاده‌شده

FILTER, GET_JALALI_MONTH_NAME, GET_JALALI_YEAR, GREG_TO_JALALI, IMPORT_FROM_SHEET, INDEX, ISBLANK, LET

> هرکدام built-in نیست، Named Function است — تعریفش را دستی از Data → Named functions بردار.


## محتوای کامل: SheetsFileIds

```
Range Name Associated	Sheets File Id
SheetsFileId_Accounting_Chalebagh	1MRTM9BV9y0bHGM79QxkE6pHhCdy45aT9hSQXGKJOWHo
```