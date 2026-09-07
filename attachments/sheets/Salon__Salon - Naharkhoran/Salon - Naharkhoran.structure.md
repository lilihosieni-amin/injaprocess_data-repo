# Salon - Naharkhoran

- spreadsheetId: `1CSidDar4ql88gHKCQT5q7mJg0Qt3LCL9_Ar_pB5pugg`
- url: https://docs.google.com/spreadsheets/d/1CSidDar4ql88gHKCQT5q7mJg0Qt3LCL9_Ar_pB5pugg/edit?usp=drivesdk
- locale: en_US | timezone: Asia/Tehran
- exported: 2026-08-29T09:27:53.602Z

## شیت‌ها

| # | نام | مخفی | ابعاد | فریز |
|---|---|---|---|---|
| 1 | تعداد فیش هرشب | - | 566×4 | 1/0 |
| 2 | ضایعات | - | 7×4 | 1/0 |
| 3 | OFF اجرایی | - | 554×4 | 1/0 |
| 4 | SheetsFileIds | **بله** | 2×2 | 1/0 |
| 5 | نیازمندیها و مشکلات | - | 482×3 | 1/0 |

## بازه‌های نام‌گذاری‌شده

- `SheetsFileId_Accounting_Chalebagh` → `SheetsFileIds!B2`

## فرمول‌های یکتا

### تعداد فیش هرشب

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
        INDEX(filteredData,,6)
      )
    ),
  result
)
`
- `D2` ×399  →  `=C2 - B2`
- `B221` ×1  →  `=LET(
  inputDate, #REF!,
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
        INDEX(filteredData,,6)
      )
    ),
  result
)
`

> اسکن فقط تا ردیف 400.

### OFF اجرایی

- `A190` ×1  →  `=SEQUENCE(365,1,A189,1)`

> اسکن فقط تا ردیف 400.

### نیازمندیها و مشکلات

- `A118` ×1  →  `=SEQUENCE(365,1,A117,1)`

> اسکن فقط تا ردیف 400.


## توابع استفاده‌شده

FILTER, GET_JALALI_MONTH_NAME, GET_JALALI_YEAR, GREG_TO_JALALI, IMPORT_FROM_SHEET, INDEX, ISBLANK, LET, SEQUENCE

> هرکدام built-in نیست، Named Function است — تعریفش را دستی از Data → Named functions بردار.


## محتوای کامل: SheetsFileIds

```
Range Name Associated	Sheets File Id
SheetsFileId_Accounting_Chalebagh	1MRTM9BV9y0bHGM79QxkE6pHhCdy45aT9hSQXGKJOWHo
```