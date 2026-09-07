# Salon - Chalebagh

- spreadsheetId: `1BzP-hyVqHVgkZekkycaPKpSDFcrdACV34oQJjb_VU9E`
- url: https://docs.google.com/spreadsheets/d/1BzP-hyVqHVgkZekkycaPKpSDFcrdACV34oQJjb_VU9E/edit?usp=drivesdk
- locale: en_US | timezone: Asia/Tehran
- exported: 2026-08-29T09:27:44.379Z

## شیت‌ها

| # | نام | مخفی | ابعاد | فریز |
|---|---|---|---|---|
| 1 | ضایعات | - | 99×4 | 1/0 |
| 2 | تعداد فیش هرشب | - | 575×4 | 1/0 |
| 3 | SheetsFileIds | **بله** | 2×2 | 1/0 |
| 4 | OFF اجرایی | - | 107×4 | 1/0 |
| 5 | نیازمندیها و مشکلات | - | 98×3 | 1/0 |

## بازه‌های نام‌گذاری‌شده

- `SheetsFileId_Accounting_Chalebagh` → `SheetsFileIds!B2`

## فرمول‌های یکتا

### تعداد فیش هرشب

- `D2` ×399  →  `=C2 - B2`
- `B3` ×398  →  `=LET(
  inputDate, A3,
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
        INDEX(filteredData,,4)
      )
    ),
  result
)`

> اسکن فقط تا ردیف 400.


## توابع استفاده‌شده

FILTER, GET_JALALI_MONTH_NAME, GET_JALALI_YEAR, GREG_TO_JALALI, IMPORT_FROM_SHEET, INDEX, ISBLANK, LET

> هرکدام built-in نیست، Named Function است — تعریفش را دستی از Data → Named functions بردار.


## محتوای کامل: SheetsFileIds

```
Range Name Associated	Sheets File Id
SheetsFileId_Accounting_Chalebagh	1MRTM9BV9y0bHGM79QxkE6pHhCdy45aT9hSQXGKJOWHo
```