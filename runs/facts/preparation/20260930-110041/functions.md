# کتابخانهٔ توابع

این فایل توسط `facts-plan build` ساخته می‌شود و هیچ ورودی‌ای در انبارهٔ داده‌ها ندارد.

## CONVERT_GR_TO_KG (named)

تعریف‌شده در: gozaresh_naharkhoran، control_gozareshat، gozaresh_markazi

فراخوانی: gozaresh_naharkhoran · پیتزا!E6، gozaresh_naharkhoran · پیتزا!F6، gozaresh_naharkhoran · پیتزا!G6، gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!L6، gozaresh_naharkhoran · پیتزا!E7، gozaresh_naharkhoran · پیتزا!F7، gozaresh_naharkhoran · پیتزا!G7، gozaresh_naharkhoran · پیتزا!I7، gozaresh_naharkhoran · پیتزا!L7، gozaresh_naharkhoran · پیتزا!E8، gozaresh_naharkhoran · پیتزا!F8، gozaresh_naharkhoran · پیتزا!G8، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!L8، gozaresh_naharkhoran · پیتزا!E9، gozaresh_naharkhoran · پیتزا!F9، gozaresh_naharkhoran · پیتزا!G9، gozaresh_naharkhoran · پیتزا!I9، gozaresh_naharkhoran · پیتزا!E10

```
LAMBDA(weight, DIVIDE(weight,1000))
```

## FILTER_BY_DATE (named)

تعریف‌شده در: gozaresh_naharkhoran، gozareshat، gozaresh_markazi

فراخوانی: gozareshat ·  تعداد فیش فروش!F6، gozareshat ·  تعداد فیش فروش!G6، gozareshat ·  تعداد فیش فروش!H6، gozareshat ·  تعداد فیش فروش!F7، gozareshat ·  تعداد فیش فروش!G7، gozareshat ·  تعداد فیش فروش!H7، gozareshat ·  تعداد فیش فروش!F9، gozareshat ·  تعداد فیش فروش!G9، gozareshat ·  تعداد فیش فروش!H9، gozareshat ·  تعداد فیش فروش!F10، gozareshat ·  تعداد فیش فروش!G10، gozareshat ·  تعداد فیش فروش!H10

```
LAMBDA(data, date, FILTER(data, INDEX(data,,1) = DATEVALUE(date)\n))
```

## FORMAT_PERSIAN_DATE (named)

تعریف‌شده در: gozaresh_naharkhoran، control_gozareshat، gozareshat، gozaresh_markazi

فراخوانی: control_gozareshat ·  تاریخ!H2، gozareshat · ضایعات!F10، gozareshat · ضایعات!I10، gozareshat · ضایعات!M10، gozareshat · ضایعات!I20، gozareshat · ضایعات!M20، gozareshat · ضایعات!I30، gozareshat · ضایعات!M30، gozareshat · نیازمندیها و مشکلات!F6، gozareshat · نیازمندیها و مشکلات!F7، gozareshat · نیازمندیها و مشکلات!F8، gozareshat · نیازمندیها و مشکلات!F9، gozareshat · نیازمندیها و مشکلات!F10، gozareshat · نیازمندیها و مشکلات!F11، gozareshat · نیازمندیها و مشکلات!F12، gozareshat · نیازمندیها و مشکلات!F13، gozareshat · نیازمندیها و مشکلات!F14، gozareshat · نیازمندیها و مشکلات!F15، gozareshat · نیازمندیها و مشکلات!F16، gozareshat · OFF اجرایی!F6

```
LAMBDA(day, month, year, TEXT(year, "0000") & "/" & TEXT(MATCH(month, {"فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"}, 0), "00") & "/" & TEXT(day, "00"))
```

## GET_CELL_VALUE_BY_PERSIAN_DATE (named)

تعریف‌شده در: gozaresh_naharkhoran، gozareshat، gozaresh_markazi

فراخوانی: gozareshat · مغایرت!E6، gozareshat · مغایرت!F6، gozareshat · مغایرت!I6، gozareshat · مغایرت!J6، gozareshat · مغایرت!E7، gozareshat · مغایرت!F7، gozareshat · مغایرت!I7، gozareshat · مغایرت!J7، gozareshat · مغایرت!E8، gozareshat · مغایرت!F8، gozareshat · مغایرت!I8، gozareshat · مغایرت!J8، gozareshat · مغایرت!E9، gozareshat · مغایرت!F9، gozareshat · مغایرت!I9، gozareshat · مغایرت!J9، gozareshat · مغایرت!E10، gozareshat · مغایرت!F10، gozareshat · مغایرت!I10، gozareshat · مغایرت!J10

```
LAMBDA(day, month, year, data, colindex, LET(\ndate,JALALI_TO_GREG(\nFORMAT_PERSIAN_DATE(day,month,year)),\n filteredData, FILTER_BY_DATE(data,date),\nINDEX(filteredData,,colindex)\n))
```

## GET_JALALI_MONTH_NAME (script)

تعریف‌شده در: Salon__Salon - Chalebagh/Salon - Chalebagh.gs، Salon__Salon - Naharkhoran/Salon - Naharkhoran.gs، Sandogh__Sandogh - NaharKhoran/Sandogh - NaharKhoran.gs، Sandogh__Sandogh - Chalebagh/Sandogh - Chalebagh.gs

فراخوانی: salon_chalebagh · تعداد فیش هرشب!B3، salon_chalebagh · تعداد فیش هرشب!B4، salon_chalebagh · تعداد فیش هرشب!B5، salon_chalebagh · تعداد فیش هرشب!B6، salon_chalebagh · تعداد فیش هرشب!B7، salon_chalebagh · تعداد فیش هرشب!B8، salon_chalebagh · تعداد فیش هرشب!B9، salon_chalebagh · تعداد فیش هرشب!B10، salon_chalebagh · تعداد فیش هرشب!B11، salon_chalebagh · تعداد فیش هرشب!B12، salon_chalebagh · تعداد فیش هرشب!B13، salon_chalebagh · تعداد فیش هرشب!B14، salon_chalebagh · تعداد فیش هرشب!B15، salon_chalebagh · تعداد فیش هرشب!B16، salon_chalebagh · تعداد فیش هرشب!B17، salon_chalebagh · تعداد فیش هرشب!B18، salon_chalebagh · تعداد فیش هرشب!B19، salon_chalebagh · تعداد فیش هرشب!B20، salon_chalebagh · تعداد فیش هرشب!B21، salon_chalebagh · تعداد فیش هرشب!B22

```
function GET_JALALI_MONTH_NAME(jalaliDateString) {
  if(!jalaliDateString) return '';
  const monthNames = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
  ];

  // Ensure the format is correct
  if (!/^1[34]\d{2}\/\d{1,2}\/\d{1,2}$/.test(jalaliDateString)) {
    return "Invalid date format";
  }

  const parts = jalaliDateString.split("/");
  const month = parseInt(parts[1], 10);

  if (month < 1 || month > 12) {
    return "Invalid month";
  }

  return monthNames[month - 1];
}
```

## GET_JALALI_YEAR (script)

تعریف‌شده در: Salon__Salon - Chalebagh/Salon - Chalebagh.gs، Salon__Salon - Naharkhoran/Salon - Naharkhoran.gs، Sandogh__Sandogh - NaharKhoran/Sandogh - NaharKhoran.gs، Sandogh__Sandogh - Chalebagh/Sandogh - Chalebagh.gs

فراخوانی: salon_chalebagh · تعداد فیش هرشب!B3، salon_chalebagh · تعداد فیش هرشب!B4، salon_chalebagh · تعداد فیش هرشب!B5، salon_chalebagh · تعداد فیش هرشب!B6، salon_chalebagh · تعداد فیش هرشب!B7، salon_chalebagh · تعداد فیش هرشب!B8، salon_chalebagh · تعداد فیش هرشب!B9، salon_chalebagh · تعداد فیش هرشب!B10، salon_chalebagh · تعداد فیش هرشب!B11، salon_chalebagh · تعداد فیش هرشب!B12، salon_chalebagh · تعداد فیش هرشب!B13، salon_chalebagh · تعداد فیش هرشب!B14، salon_chalebagh · تعداد فیش هرشب!B15، salon_chalebagh · تعداد فیش هرشب!B16، salon_chalebagh · تعداد فیش هرشب!B17، salon_chalebagh · تعداد فیش هرشب!B18، salon_chalebagh · تعداد فیش هرشب!B19، salon_chalebagh · تعداد فیش هرشب!B20، salon_chalebagh · تعداد فیش هرشب!B21، salon_chalebagh · تعداد فیش هرشب!B22

```
function GET_JALALI_YEAR(jalaliDateString) {
  if(!jalaliDateString) return '';
  if (!/^1[34]\d{2}\/\d{1,2}\/\d{1,2}$/.test(jalaliDateString)) {
    return "Invalid date format";
  }

  const parts = jalaliDateString.split("/");
  return parseInt(parts[0], 10);
}
```

## GET_ROW_BY_PERSIAN_DATE (named)

تعریف‌شده در: gozaresh_naharkhoran، gozaresh_markazi

فراخوانی: gozaresh_naharkhoran · پیتزا!E6، gozaresh_naharkhoran · پیتزا!F6، gozaresh_naharkhoran · پیتزا!G6، gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!K6، gozaresh_naharkhoran · پیتزا!E7، gozaresh_naharkhoran · پیتزا!F7، gozaresh_naharkhoran · پیتزا!G7، gozaresh_naharkhoran · پیتزا!I7، gozaresh_naharkhoran · پیتزا!K7، gozaresh_naharkhoran · پیتزا!E8، gozaresh_naharkhoran · پیتزا!F8، gozaresh_naharkhoran · پیتزا!G8، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!K8، gozaresh_naharkhoran · پیتزا!E9، gozaresh_naharkhoran · پیتزا!F9، gozaresh_naharkhoran · پیتزا!G9، gozaresh_naharkhoran · پیتزا!I9، gozaresh_naharkhoran · پیتزا!K9

```
LAMBDA(day, month, year, data, LET(\n  persianDate, FORMAT_PERSIAN_DATE(day, month, year),\n  header, INDEX(data, 1),\n  isCombinedDateFormat, IS_COMBINED_PERSIAN_DATE(INDEX(data,2, 1)),\n  \n  IF(\n    isCombinedDateFormat,\n    VSTACK(header, FILTER(data, INDEX(data,,1) = persianDate)),\n    VSTACK(header, FILTER(data, FORMAT_PERSIAN_DATE(INDEX(data, ,1), INDEX(data, ,2), INDEX(data, ,3)) = persianDate))\n  )\n))
```

## GREG_TO_JALALI (script)

تعریف‌شده در: Salon__Salon - Chalebagh/Salon - Chalebagh.gs، Salon__Salon - Naharkhoran/Salon - Naharkhoran.gs، Sandogh__Sandogh - NaharKhoran/Sandogh - NaharKhoran.gs، Sandogh__Sandogh - Chalebagh/Sandogh - Chalebagh.gs

فراخوانی: salon_chalebagh · تعداد فیش هرشب!B3، salon_chalebagh · تعداد فیش هرشب!B4، salon_chalebagh · تعداد فیش هرشب!B5، salon_chalebagh · تعداد فیش هرشب!B6، salon_chalebagh · تعداد فیش هرشب!B7، salon_chalebagh · تعداد فیش هرشب!B8، salon_chalebagh · تعداد فیش هرشب!B9، salon_chalebagh · تعداد فیش هرشب!B10، salon_chalebagh · تعداد فیش هرشب!B11، salon_chalebagh · تعداد فیش هرشب!B12، salon_chalebagh · تعداد فیش هرشب!B13، salon_chalebagh · تعداد فیش هرشب!B14، salon_chalebagh · تعداد فیش هرشب!B15، salon_chalebagh · تعداد فیش هرشب!B16، salon_chalebagh · تعداد فیش هرشب!B17، salon_chalebagh · تعداد فیش هرشب!B18، salon_chalebagh · تعداد فیش هرشب!B19، salon_chalebagh · تعداد فیش هرشب!B20، salon_chalebagh · تعداد فیش هرشب!B21، salon_chalebagh · تعداد فیش هرشب!B22

```
function GREG_TO_JALALI(dateInput) {
  if(!dateInput) return "";
  if (!(dateInput instanceof Date)) return "Invalid date";

  const gy = dateInput.getFullYear();
  const gm = dateInput.getMonth() + 1; // JavaScript months are 0-based
  const gd = dateInput.getDate();

  const [jy, jm, jd] = gregorianToJalali(gy, gm, gd);
  return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;
}
```

## IMPORT_FROM_SHEET (named)

تعریف‌شده در: salon_chalebagh، salon_naharkhoran، gozaresh_naharkhoran، sandogh_naharkhoran، sandogh_chalebagh، control_gozareshat، gozareshat، gozaresh_markazi

فراخوانی: salon_chalebagh · تعداد فیش هرشب!B3، salon_chalebagh · تعداد فیش هرشب!B4، salon_chalebagh · تعداد فیش هرشب!B5، salon_chalebagh · تعداد فیش هرشب!B6، salon_chalebagh · تعداد فیش هرشب!B7، salon_chalebagh · تعداد فیش هرشب!B8، salon_chalebagh · تعداد فیش هرشب!B9، salon_chalebagh · تعداد فیش هرشب!B10، salon_chalebagh · تعداد فیش هرشب!B11، salon_chalebagh · تعداد فیش هرشب!B12، salon_chalebagh · تعداد فیش هرشب!B13، salon_chalebagh · تعداد فیش هرشب!B14، salon_chalebagh · تعداد فیش هرشب!B15، salon_chalebagh · تعداد فیش هرشب!B16، salon_chalebagh · تعداد فیش هرشب!B17، salon_chalebagh · تعداد فیش هرشب!B18، salon_chalebagh · تعداد فیش هرشب!B19، salon_chalebagh · تعداد فیش هرشب!B20، salon_chalebagh · تعداد فیش هرشب!B21، salon_chalebagh · تعداد فیش هرشب!B22

```
LAMBDA(sheetsfileid, sheetname, datarange, IMPORTRANGE("https://docs.google.com/spreadsheets/d/" & sheetsfileid, sheetname & "!" & datarange))
```

## IS_COMBINED_PERSIAN_DATE (named)

تعریف‌شده در: gozaresh_naharkhoran، gozaresh_markazi

فراخوانی: —

```
LAMBDA(datestring, REGEXMATCH(TO_TEXT(datestring), "^\\d{4}/\\d{2}/\\d{2}$"))
```

## JALALI_TO_GREG (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozareshat · ضایعات!F10، gozareshat · ضایعات!I10، gozareshat · ضایعات!M10، gozareshat · ضایعات!I20، gozareshat · ضایعات!M20، gozareshat · ضایعات!I30، gozareshat · ضایعات!M30، gozareshat · نیازمندیها و مشکلات!F6، gozareshat · نیازمندیها و مشکلات!F7، gozareshat · نیازمندیها و مشکلات!F8، gozareshat · نیازمندیها و مشکلات!F9، gozareshat · نیازمندیها و مشکلات!F10، gozareshat · نیازمندیها و مشکلات!F11، gozareshat · نیازمندیها و مشکلات!F12، gozareshat · نیازمندیها و مشکلات!F13، gozareshat · نیازمندیها و مشکلات!F14، gozareshat · نیازمندیها و مشکلات!F15، gozareshat · نیازمندیها و مشکلات!F16، gozareshat · OFF اجرایی!F6، gozareshat · OFF اجرایی!F7

```
function JALALI_TO_GREG(jalaliStr) {
  if(!jalaliStr) return '';
  var parts = jalaliStr.split('/');
  var jy = parseInt(parts[0], 10);
  var jm = parseInt(parts[1], 10);
  var jd = parseInt(parts[2], 10);
  var date = jalaliToGregorian(jy, jm, jd);
  return Utilities.formatDate(date, Session.getScriptTimeZone(), "MM/dd/yyyy");
}
```

## PERSIAN_WEEKDAY (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · Copy of مواد حساس!J3، control_gozareshat · Copy of مواد حساس!N4، control_gozareshat · Copy of مواد حساس!J5، control_gozareshat · Copy of مواد حساس!J9، control_gozareshat · Copy of مواد حساس!H13

```
function PERSIAN_WEEKDAY(jdate) {
  var p = String(jdate).split("/");
  var g = persianToGregorian(Number(p[0]), Number(p[1]), Number(p[2]));

  return Utilities.formatDate(g, Session.getScriptTimeZone(), "EEEE");
}
```

## calcBuffer (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!J3، control_gozareshat · مواد حساس!J4، control_gozareshat · مواد حساس!J5، control_gozareshat · مواد حساس!J6، control_gozareshat · مواد حساس!J7، control_gozareshat · مواد حساس!J8، control_gozareshat · مواد حساس!J9، control_gozareshat · مواد حساس!J10، control_gozareshat · مواد حساس!J11، control_gozareshat · مواد حساس!J12، control_gozareshat · مواد حساس!J13، control_gozareshat · مواد حساس!J14، control_gozareshat · مواد حساس!J15، control_gozareshat · مواد حساس!J16، control_gozareshat · مواد حساس!J17، control_gozareshat · مواد حساس!J18، control_gozareshat · مواد حساس!J19، control_gozareshat · مواد حساس!J20، control_gozareshat · مواد حساس!J21، control_gozareshat · مواد حساس!J22

```
function calcBuffer(avg,previousDay) {
  return Math.max((avg*20)/100,(previousDay*30)/100)
}


**********************************************************************************
Dialog.html:

<!DOCTYPE html>
<html dir="rtl">

<head>
  <base target="_top">

  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap" rel="stylesheet">

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: #f4f6fb;
      font-family: 'Vazirmatn', Tahoma, sans-serif;
      color: #333;
    }

    .header {
      background: #1976d2;
      color: white;
      padding: 18px;
      text-align: center;
      font-size: 22px;
      font-weight: 700;
      box-shadow: 0 2px 10px rgba(0, 0, 0, .15);
    }

    .container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      padding: 22px;
    }

    .panel {
      background: white;
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, .08);
      min-height: 420px;
    }

    h3 {
      margin-top: 0;
      color: #1976d2;
      font-size: 18px;
    }

    .summaryRow {
      margin-bottom: 16px;
    }

    .summaryTitle {
      color: #888;
      font-size: 13px;
      margin-bottom: 6px;
    }

    .summaryValue {
      font-size: 17px;
      font-weight: 600;
    }

    #events {
      min-height: 100px;
      background: #f8fafc;
      border-radius: 12px;
      padding: 12px;
    }

    .event {
      padding: 5px 0;
    }

    .factor {
      margin-top: 20px;
      text-align: center;
      background: #e3f2fd;
      color: #1565c0;
      border-radius: 14px;
      padding: 18px;
    }

    .factor small {
      display: block;
      font-size: 13px;
      color: #777;
      margin-bottom: 8px;
    }

    .factorValue {
      font-size: 34px;
      font-weight: bold;
    }

    .card {
      border: 2px solid #e3e8ef;
      border-radius: 14px;
      padding: 16px;
      margin-bottom: 12px;
      cursor: pointer;
      transition: .2s;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
    }

    .card:hover {
      border-color: #2196f3;
      transform: translateY(-2px);
    }

    .card.selected {
      border-color: #1976d2;
      background: #eaf4ff;
    }

    .left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .check {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 2px solid #bbb;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 13px;
      color: white;
      transition: .2s;
    }

    .selected .check {
      background: #1976d2;
      border-color: #1976d2;
    }

    .percent {
      font-weight: bold;
      color: #1976d2;
    }

    button {
      width: 100%;
      margin-top: 20px;
      border: none;
      background: #2e7d32;
      color: white;
      padding: 15px;
      font-size: 16px;
      border-radius: 12px;
      cursor: pointer;
      font-family: inherit;
      transition: .2s;
    }

    button:hover {
      background: #1b5e20;
    }

    /* @media(max-width:850px){
      .container{
        grid-template-columns:1fr 1fr;
      }
    } */
  </style>
</head>

<body>

  <!-- <div class="header">
ثبت سفارش مواد حساس
</div> -->

  <div class="container">

    <div class="panel">

      <h3>خلاصه</h3>

      <div class="summaryRow">
        <div class="summaryTitle">تاریخ</div>
        <div class="summaryValue" id="date">...</div>
      </div>

      <div class="summaryRow">
        <div class="summaryTitle">رویدادهای انتخاب شده</div>
        <div id="events">
          بدون ضریب
        </div>
      </div>

      <div class="factor">
        <small>ضریب نهایی</small>
        <div class="factorValue" id="factor">×1.000</div>
      </div>

      <button onclick="submitOrder()">
ثبت سفارش
</button>

    </div>

    <div class="panel">

      <h3>شرایط امروز</h3>

      <div class="card" data-key="tomorrowHoliday" data-title="تعطیلی روز آینده" data-factor="1.10">
        <div class="left">
          <div class="check"></div>
          <div>تعطیلی روز آینده</div>
        </div>
        <div class="percent">+10%</div>
      </div>

      <div class="card" data-key="mourning" data-title="عزای عمومی" data-factor="0.90">
        <div class="left">
          <div class="check"></div>
          <div>عزای عمومی</div>
        </div>
        <div class="percent">−10%</div>
      </div>

      <div class="card" data-key="ramadan" data-title="ماه رمضان" data-factor="0.80">
        <div class="left">
          <div class="check"></div>
          <div>ماه رمضان</div>
        </div>
        <div class="percent">−20%</div>
      </div>

      <div class="card" data-key="competitorHoliday" data-title="تعطیلی رقیب اصلی" data-factor="1.05">
        <div class="left">
          <div class="check"></div>
          <div>تعطیلی رقیب اصلی</div>
        </div>
        <div class="percent">+5%</div>
      </div>

    </div>

  </div>

  <script>
    let selected=[];

google.script.run.withSuccessHandler(function(info){
    document.getElementById("date").textContent=info.date;
}).getSummary([]);

document.querySelectorAll(".card").forEach(card=>{

    card.onclick=function(){

        card.classList.toggle("selected");

        if(card.classList.contains("selected"))
            card.querySelector(".check").innerHTML="✓";
        else
            card.querySelector(".check").innerHTML="";

        updateSummary();

    };

});
```

## categorizeFoodData (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function categorizeFoodData(parsedData, foodIdToCategory) {
  let result = {};

  Object.keys(foodIdToCategory).forEach(function(category) {
    result[foodIdToCategory[category]] = {};
  });

  parsedData.forEach(function(row) {
    const foodId = row[3];  // "كد كالا" is in the 4th column (index 3)
    const foodCount = row[2]; // "تعداد" is in the 3rd column (index 2)

    // Find the category for the given foodId
    const category = foodIdToCategory[foodId];

    if (category) {
      if (result[category]) {
        if (result[category][foodId]) {
          result[category][foodId] += foodCount;  // Increment food count
        } else {
          result[category][foodId] = foodCount;  // Set food count for the first time
        }
      }
    }
  });

  return result;
}




**********************************************************************************
updateFoodCount.gs:
```

## extractFoodIdFromHeader (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function extractFoodIdFromHeader(header) {
  const match = header.match(/#(\d+)/);
  return match ? parseInt(match[1], 10) : null;
}
**********************************************************************************
uploadFileDialog.html:

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Upload Sales Data</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment-jalaali/0.9.1/moment-jalaali.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js"></script>
  <style>
    *, *::after, *::before {
      box-sizing: border-box;
    }
    body {
      font-family: 'Inter', sans-serif;
      background-color: #fff;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    h2 {
      color: #333;
      font-size: 24px;
    }

    label {
      font-size: 16px;
      color: #555;
      margin-bottom: 8px;
      display: block;
    }

    /* Input fields */
    input[type="date"], input[type="file"], select {
      width: 100%;
      padding: 12px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: #f9fafb;
      font-size: 16px;
      color: #333;
      transition: border-color 0.2s ease;
    }

    input[type="date"]:focus, input[type="file"]:focus, select:focus {
      border-color: #3b82f6;
    }

    /* Button styles */
    #uploadButton {
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #3b82f6;
      color: #fff;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
      width: 100%;
      transition: background-color 0.3s ease, transform 0.2s ease;
    }

    #uploadButton:disabled {
      background-color: #9ca3af;
      cursor: not-allowed;
    }

    #uploadButton:hover:enabled {
      background-color: #2563eb;
    }

    /* File preview table */
    table {
      width: 100%;
      margin-top: 16px;
      border-collapse: collapse;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    table th, table td {
      padding: 8px 12px;
      text-align: left;
      border-bottom: 1px solid #e5e7eb;
    }

    table th {
      background-color: #f3f4f6;
      color: #333;
    }

    /* Loading spinner */
    .spinner {
      display: inline-block;
      width: 24px;
      height: 24px;
      border: 2px solid #f3f4f6;
      border-top: 2px solid #3b82f6;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    .stack {
      display:flex;
      flex-direction: column;
    }

    .group {
      display:flex;
      flex-direction: row;
      justify-content: space-between;
    }

    .gap-50 {
      gap: 50px;
    }


    .inputFields {
      gap: 30px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="stack gap-50">
      <h2>Upload Sales Data (.xlsx)</h2>
    
      <div class="stack inputFields">
        <div class="group">
          <div>
            <label for="day">Day:</label>
            <select id="day" name="day">
              <!-- Days from 1 to 31 -->
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
              <option value="11">11</option>
              <option value="12">12</option>
              <option value="13">13</option>
              <option value="14">14</option>
              <option value="15">15</option>
              <option value="16">16</option>
              <option value="17">17</option>
              <option value="18">18</option>
              <option value="19">19</option>
              <option value="20">20</option>
              <option value="21">21</option>
              <option value="22">22</option>
              <option value="23">23</option>
              <option value="24">24</option>
              <option value="25">25</option>
              <option value="26">26</option>
              <option value="27">27</option>
              <option value="28">28</option>
              <option value="29">29</option>
              <option value="30">30</option>
              <option value="31">31</option>
            </select>
          </div>
          <div>
            <label for="month">Month:</label>
            <select id="month" name="month">
              <option value="1">فروردین</option>
              <option value="2">اردیبهشت</option>
              <option value="3">خرداد</option>
              <option value="4">تیر</option>
              <option value="5">مرداد</option>
              <option value="6">شهریور</option>
              <option value="7">مهر</option>
              <option value="8">آبان</option>
              <option value="9">آذر</option>
              <option value="10">دی</option>
              <option value="11">بهمن</option>
              <option value="12">اسفند</option>
            </select>
          </div>
          <div>
            <label for="year">Year:</label>
            <select id="year" name="year">
              <option value="1404">1404</option>
              <option value="1405">1405</option>
              <option value="1406">1406</option>
              <option value="1407">1407</option>
              <option value="1408">1408</option>
              <option value="1409">1409</option>
              <option value="1410">1410</option>
              <option value="1411">1411</option>
              <option value="1412">1412</option>
              <option value="1413">1413</option>
              <option value="1414">1414</option>
              <option value="1415">1415</option>
              <option value="1416">1416</option>
              <option value="1417">1417</option>
              <option value="1418">1418</option>
              <option value="1419">1419</option>
              <option value="1420">1420</option>
            </select>
          </div>
        </div>

        <div>
          <label for="fileInput">Choose file:</label>
          <input type="file" id="fileInput" accept=".xlsx" required/>
        </div>
      </div>
    
      <button id="uploadButton" onclick="uploadFile()">Upload File</button>
    
      <div id="filePreview"></div>

  </div>

  <script>
    function uploadFile() {
      const file = document.getElementById('fileInput').files[0];
      if (!file) {
        alert("Please select a file to upload.");
        return;
      }
      const dayInput = document.getElementById('day').value
      const monthInput = document.getElementById('month').value
      const yearInput = document.getElementById('year').value

      if (!Boolean(dayInput) || !Boolean(monthInput) || !Boolean(yearInput) ) {
        alert("Please enter date");
        return;
      }
      const formattedDate = [yearInput,monthInput,dayInput].map(el=> el.padStart(2, "0")).join("/");
      
      const uploadButton = document.getElementById('uploadButton');
      uploadButton.disabled = true;
      uploadButton.innerHTML = '<div class="spinner"><div>';

      const reader = new FileReader();
      reader.onload = function(e) {
        const data = e.target.result;
        const workbook = XLSX.read(data, { type: 'binary' });

        // You can specify the sheet name or just get the first sheet
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

        // Pass the file data to the Apps Script function for further processing
        google.script.run.withSuccessHandler(function(response) {
          uploadButton.disabled = false;
          uploadButton.innerHTML = 'Done ✅';
          console.log(response);
          setTimeout(function() {
            uploadButton.innerHTML = 'Upload File';
            document.getElementById('fileInput').value = '';
          }, 2000);
        }).logFormData(jsonData,formattedDate);
      };

      reader.readAsBinaryString(file);
    }
  </script>
</body>
</html>


**********************************************************************************
```

## extractFoodIds (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function extractFoodIds(headerRow) {
  // Handle both 1D and 2D arrays
  const headers = Array.isArray(headerRow[0]) ? headerRow[0] : headerRow;

  return headers
    .map(cell => {
      const match = String(cell).match(/#(\d+)$/);
      return match ? Number(match[1]) : null;
    })
    .filter(id => id !== null);
}
```

## getAverage (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!F3، control_gozareshat · مواد حساس!F4، control_gozareshat · مواد حساس!F5، control_gozareshat · مواد حساس!F6، control_gozareshat · مواد حساس!F7، control_gozareshat · مواد حساس!F8، control_gozareshat · مواد حساس!F9، control_gozareshat · مواد حساس!F10، control_gozareshat · مواد حساس!F11، control_gozareshat · مواد حساس!F12، control_gozareshat · مواد حساس!F13، control_gozareshat · مواد حساس!F14، control_gozareshat · مواد حساس!F15، control_gozareshat · مواد حساس!F16، control_gozareshat · مواد حساس!F17، control_gozareshat · مواد حساس!F18، control_gozareshat · مواد حساس!F19، control_gozareshat · مواد حساس!F20، control_gozareshat · مواد حساس!F21، control_gozareshat · مواد حساس!F22

```
function getAverage(data) {
  let total = 0;
  let validDays = 0;

  for (const day of data) {
    let dayTotal = 0;
    let hasData = false;

    for (const value of day) {
      if (typeof value === "number") {
        dayTotal += value;
        hasData = true;
      }
    }

    if (hasData) {
      total += dayTotal;
      validDays++;
    }
  }

  return validDays ? Math.ceil(total / validDays) : "N/A";
}


**********************************************************************************
date.gs:
```

## getFoodValueById (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، Gozareshat/Gozareshat.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!I11، gozaresh_naharkhoran · پیتزا!I12، gozaresh_naharkhoran · پیتزا!I14، gozaresh_naharkhoran · کانتر!I6، gozaresh_naharkhoran · کانتر!I7، gozaresh_naharkhoran · کانتر!I8، gozaresh_naharkhoran · کانتر!I9، gozaresh_naharkhoran · کانتر!I10، gozaresh_markazi · پیتزا!I6، gozaresh_markazi · پیتزا!I8، gozaresh_markazi · پیتزا!I11، gozaresh_markazi · پیتزا!I12، gozaresh_markazi · پیتزا!I14، gozaresh_markazi · کانتر!I6، gozaresh_markazi · کانتر!I7، gozaresh_markazi · کانتر!I8، gozaresh_markazi · کانتر!I9، gozaresh_markazi · کانتر!I10

```
function getFoodValueById(foodId, data,refresher="") {
  return getValueById(foodId,data,'#')
}
```

## getIngredientValue (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!I11، gozaresh_naharkhoran · پیتزا!I12، gozaresh_naharkhoran · پیتزا!I14، gozaresh_markazi · پیتزا!I6، gozaresh_markazi · پیتزا!I8، gozaresh_markazi · پیتزا!I11، gozaresh_markazi · پیتزا!I12، gozaresh_markazi · پیتزا!I14

```
function getIngredientValue(foodId, ingredientId, ingredientsNamedRange, refresher = "") {
  const range = SpreadsheetApp.getActiveSpreadsheet().getRangeByName(ingredientsNamedRange);
  if (!range) {
    return "Error: Named range '" + ingredientsNamedRange + "' not found!";
  }
  const data = range.getValues();

  const foodIdString = '#' + foodId;
  const ingredientIdString = '##' + ingredientId;


  let foodRow = -1;
  for (var i = 1; i < data.length; i++) {
    if (data[i][0].toString().includes(foodIdString)) {
      foodRow = i;
      break;
    }
  }

  if (foodRow === -1) {
    return "Food ID " + foodId + " not found!";
  }

  let ingredientColumn = -1;
  for (var j = 1; j < data[0].length; j++) {
    if (data[0][j].toString().includes(ingredientIdString)) {
      ingredientColumn = j;
      break;
    }
  }

  if (ingredientColumn === -1) {
    return "Ingredient ID " + ingredientId + " not found!";
  }

  return data[foodRow][ingredientColumn];
}
```

## getIngredientValue (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!I11، gozaresh_naharkhoran · پیتزا!I12، gozaresh_naharkhoran · پیتزا!I14، gozaresh_markazi · پیتزا!I6، gozaresh_markazi · پیتزا!I8، gozaresh_markazi · پیتزا!I11، gozaresh_markazi · پیتزا!I12، gozaresh_markazi · پیتزا!I14

```
function getIngredientValue(foodId, ingredientId, namedRange, refresher="") {
  const range = SpreadsheetApp.getActiveSpreadsheet().getRangeByName(namedRange);
  if (!range) {
    return "Error: Named range '" + namedRange + "' not found!";
  }
  const data = range.getValues();
  
  const foodIdString = '#' + foodId; 
  const ingredientIdString = '##' + ingredientId; 

  
  let foodRow = -1;
  for (var i = 1; i < data.length; i++) {
    if (data[i][0].toString().includes(foodIdString)) {
      foodRow = i;
      break;
    }
  }
  
  if (foodRow === -1) {
    return "Food ID " + foodId + " not found!";
  }
  
  let ingredientColumn = -1;
  for (var j = 1; j < data[0].length; j++) {
    if (data[0][j].toString().includes(ingredientIdString)) {
      ingredientColumn = j;
      break;
    }
  }
  
  if (ingredientColumn === -1) {
    return "Ingredient ID " + ingredientId + " not found!";
  }
  
  return data[foodRow][ingredientColumn];
}
```

## getIngredientValueById (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، Gozareshat/Gozareshat.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!E6، gozaresh_naharkhoran · پیتزا!F6، gozaresh_naharkhoran · پیتزا!G6، gozaresh_naharkhoran · پیتزا!E7، gozaresh_naharkhoran · پیتزا!F7، gozaresh_naharkhoran · پیتزا!G7، gozaresh_naharkhoran · پیتزا!E8، gozaresh_naharkhoran · پیتزا!F8، gozaresh_naharkhoran · پیتزا!G8، gozaresh_naharkhoran · پیتزا!E9، gozaresh_naharkhoran · پیتزا!F9، gozaresh_naharkhoran · پیتزا!G9، gozaresh_naharkhoran · پیتزا!E10، gozaresh_naharkhoran · پیتزا!F10، gozaresh_naharkhoran · پیتزا!G10، gozaresh_naharkhoran · پیتزا!E11، gozaresh_naharkhoran · پیتزا!F11، gozaresh_naharkhoran · پیتزا!G11، gozaresh_naharkhoran · پیتزا!E12، gozaresh_naharkhoran · پیتزا!F12

```
function getIngredientValueById(ingredientId, data,refresher="") {
  return getValueById(ingredientId,data,'##')
}
```

## getLast3DaysRows (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!G3، control_gozareshat · مواد حساس!G4، control_gozareshat · مواد حساس!G5، control_gozareshat · مواد حساس!G6، control_gozareshat · مواد حساس!G7، control_gozareshat · مواد حساس!G8، control_gozareshat · مواد حساس!G9، control_gozareshat · مواد حساس!G10، control_gozareshat · مواد حساس!G11، control_gozareshat · مواد حساس!G12، control_gozareshat · مواد حساس!G13، control_gozareshat · مواد حساس!G14، control_gozareshat · مواد حساس!G15، control_gozareshat · مواد حساس!G16، control_gozareshat · مواد حساس!G17، control_gozareshat · مواد حساس!G18، control_gozareshat · مواد حساس!G19، control_gozareshat · مواد حساس!G20، control_gozareshat · مواد حساس!G21، control_gozareshat · مواد حساس!G22

```
function getLast3DaysRows(data, targetDate) {
  const targetGregorian = persianToGregorianDate(targetDate);

  const startGregorian = new Date(targetGregorian);
  startGregorian.setDate(startGregorian.getDate() - 3);

  const result = [];
  const res = [];

  for (let i = data.length - 1; i >= 1; i--) {
    const row = data[i];
    const rowDateStr = row[0];

    if (!rowDateStr) continue;

    const rowGregorian = persianToGregorianDate(rowDateStr);

    // row is after target date
    if (rowGregorian >= targetGregorian) {
      continue;
    }

    // optimization:
    // since table is sorted ascending,
    // once we're older than start date we can stop
    if (rowGregorian < startGregorian) {
      break;
    }

    result.push(row);

  }

  return [
    data[0],
    ...result.reverse()
  ];
}

//###########################
```

## getPreviousDayRow (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!I3، control_gozareshat · مواد حساس!J3، control_gozareshat · مواد حساس!I4، control_gozareshat · مواد حساس!J4، control_gozareshat · مواد حساس!I5، control_gozareshat · مواد حساس!J5، control_gozareshat · مواد حساس!I6، control_gozareshat · مواد حساس!J6، control_gozareshat · مواد حساس!I7، control_gozareshat · مواد حساس!J7، control_gozareshat · مواد حساس!I8، control_gozareshat · مواد حساس!J8، control_gozareshat · مواد حساس!I9، control_gozareshat · مواد حساس!J9، control_gozareshat · مواد حساس!I10، control_gozareshat · مواد حساس!J10، control_gozareshat · مواد حساس!I11، control_gozareshat · مواد حساس!J11، control_gozareshat · مواد حساس!I12، control_gozareshat · مواد حساس!J12

```
function getPreviousDayRow(data, targetDate) {
  const targetGregorian = persianToGregorianDate(targetDate);

  // Previous day
  const previousDate = new Date(targetGregorian);
  previousDate.setDate(previousDate.getDate() - 1);

  const previousPersianDate = gregorianToPersianDate(previousDate);

  // Split yyyy/mm/dd
  const [year, month, day] = previousPersianDate.split("/");

  // Persian month names
  const persianMonths = [
    "",
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند"
  ];

  const columnCount = data[0].length;

  // Determine table format
  const firstDataCell = String(data[1]?.[0] ?? "");

  if (isValidPersianDate(firstDataCell)) {
    // ===== Single date column =====
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]) === previousPersianDate) {
        return [data[0], data[i]];
      }
    }

    // Not found
    const newRow = new Array(columnCount).fill("N/A");
    newRow[0] = previousPersianDate;

    return [data[0], newRow];

  } else {
    // ===== Three columns: روز | ماه | سال =====
    const monthName = persianMonths[Number(month)];

    for (let i = 1; i < data.length; i++) {
      const row = data[i];

      if (
        Number(row[0]) === Number(day) &&
        String(row[1]) === monthName &&
        Number(row[2]) === Number(year)
      ) {
        return [data[0], row];
      }
    }

    // Not found
    const newRow = new Array(columnCount).fill("N/A");
    newRow[0] = Number(day);
    newRow[1] = monthName;
    newRow[2] = Number(year);

    return [data[0], newRow];
  }
}
```

## getPreviousDayRow2 (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function getPreviousDayRow2(data, targetDate) {
  const targetGregorian = persianToGregorianDate(targetDate);

  // Previous day
  const previousDate = new Date(targetGregorian);
  previousDate.setDate(previousDate.getDate() - 1);

  const previousPersianDate = gregorianToPersianDate(previousDate);

  const columnCount = data[0].length;

  // Skip header and look for the row
  for (let i = 1; i < data.length; i++) {
    const row = data[i];

    if (row[0] === previousPersianDate) {
      return [
        data[0],
        row
      ];
    }
  }

  // If the previous day doesn't exist, return a synthetic row
  const newRow = new Array(columnCount).fill("N/A");
  newRow[0] = previousPersianDate;

  return [
    data[0],
    newRow
  ];
}
```

## getSameWeekdayRowsLast30Days (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!F3، control_gozareshat · مواد حساس!F4، control_gozareshat · مواد حساس!F5، control_gozareshat · مواد حساس!F6، control_gozareshat · مواد حساس!F7، control_gozareshat · مواد حساس!F8، control_gozareshat · مواد حساس!F9، control_gozareshat · مواد حساس!F10، control_gozareshat · مواد حساس!F11، control_gozareshat · مواد حساس!F12، control_gozareshat · مواد حساس!F13، control_gozareshat · مواد حساس!F14، control_gozareshat · مواد حساس!F15، control_gozareshat · مواد حساس!F16، control_gozareshat · مواد حساس!F17، control_gozareshat · مواد حساس!F18، control_gozareshat · مواد حساس!F19، control_gozareshat · مواد حساس!F20، control_gozareshat · مواد حساس!F21، control_gozareshat · مواد حساس!F22

```
function getSameWeekdayRowsLast30Days(data, targetDate) {
  const targetGregorian = persianToGregorianDate(targetDate);

  const startGregorian = new Date(targetGregorian);
  startGregorian.setDate(startGregorian.getDate() - 30);

  const startTime = startGregorian.getTime();

  // Map existing rows by Persian date
  const rowsByDate = new Map();

  // Skip header
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (row[0]) {
      rowsByDate.set(row[0], row);
    }
  }

  const result = [];
  const columnCount = data[0].length;

  // Go back one week at a time
  for (let daysBack = 7; ; daysBack += 7) {
    const date = new Date(targetGregorian);
    date.setDate(date.getDate() - daysBack);

    if (date.getTime() < startTime) {
      break;
    }

    const persianDate = gregorianToPersianDate(date);

    const existingRow = rowsByDate.get(persianDate);

    if (existingRow) {
      result.push(existingRow);
    } else {
      // Create a synthetic row with zeros
      const newRow = new Array(columnCount).fill("N/A");
      newRow[0] = persianDate;
      result.push(newRow);
    }
  }

  // Oldest → newest (same order as your original function)
  result.reverse();

  return [
    data[0], // Header row
    ...result
  ];
}
```

## getSummary (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function getSummary(selectedEvents) {

  let coefficient = 1;
  let titles = [];

  selectedEvents.forEach(key => {
    if (EVENTS[key]) {
      coefficient *= EVENTS[key].factor;
      titles.push(EVENTS[key].title);
    }
  });

  const ss = SpreadsheetApp.getActive();

  const date = ss.getRangeByName("Date").getDisplayValue();

  const source = ss.getSheetByName(SOURCE_SHEET);

  const values = source.getRange(2,4,source.getLastRow()-1,8).getValues();

  let count = 0;

  values.forEach(r=>{
    if(r[7] !== "" && r[7] != null)
      count++;
  });

  return {
    date,
    coefficient,
    coefficientText: coefficient.toFixed(3),
    events: titles,
    count
  };

}
```

## getTotalFoodsCountsInRowById (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!K6، gozaresh_naharkhoran · پیتزا!K7، gozaresh_naharkhoran · پیتزا!K8، gozaresh_naharkhoran · پیتزا!K9، gozaresh_naharkhoran · پیتزا!K10، gozaresh_naharkhoran · پیتزا!K11، gozaresh_naharkhoran · پیتزا!K12، gozaresh_naharkhoran · پیتزا!K13، gozaresh_naharkhoran · پیتزا!K14، gozaresh_naharkhoran · پیتزا!K15، gozaresh_naharkhoran · فرنگی!K6، gozaresh_naharkhoran · فرنگی!K7، gozaresh_naharkhoran · فرنگی!K8، gozaresh_naharkhoran · فرنگی!K9، gozaresh_naharkhoran · فرنگی!K10، gozaresh_naharkhoran · فرنگی!K11، gozaresh_naharkhoran · فرنگی!K12، gozaresh_naharkhoran · فرنگی!K13، gozaresh_naharkhoran · فرنگی!K14، gozaresh_markazi · پیتزا!K6

```
function getTotalFoodsCountsInRowById(foodIds, salesData,refresher="") {
  if(typeof foodIds === "number"){
    return getFoodValueById(foodIds,salesData);
  }
  const arr = foodIds[0].map(foodId => {
    return getFoodValueById(foodId,salesData);
  });
 return arr.filter(x=>Boolean(x)).reduce((acc, currentValue) => acc + currentValue,0);
}



**********************************************************************************
```

## getTotalFoodsIngredient (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!I7، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!I9، gozaresh_naharkhoran · پیتزا!I10، gozaresh_naharkhoran · پیتزا!I11، gozaresh_naharkhoran · پیتزا!I13، gozaresh_naharkhoran · پیتزا!I15، gozaresh_naharkhoran · فرنگی!I6، gozaresh_naharkhoran · فرنگی!I7، gozaresh_naharkhoran · فرنگی!I8، gozaresh_naharkhoran · فرنگی!I9، gozaresh_naharkhoran · فرنگی!I10، gozaresh_naharkhoran · فرنگی!I11، gozaresh_naharkhoran · فرنگی!I12، gozaresh_naharkhoran · فرنگی!I13، gozaresh_naharkhoran · فرنگی!I14، gozaresh_naharkhoran · سوخاری!I6، gozaresh_naharkhoran · سوخاری!I7، gozaresh_naharkhoran · سوخاری!I8

```
function getTotalFoodsIngredient(
  foodIds,
  ingredientId,
  salesRows,
  ingredientNamedRange,
  refresher = "",
) {
  const x = getTotalFoodsIngredientPerDay(
    foodIds,
    ingredientId,
    salesRows,
    ingredientNamedRange,
    refresher
  )

  return x.reduce((acc, currentValue) => acc + currentValue, 0)
}
```

## getTotalFoodsIngredient (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: gozaresh_naharkhoran · پیتزا!I6، gozaresh_naharkhoran · پیتزا!I7، gozaresh_naharkhoran · پیتزا!I8، gozaresh_naharkhoran · پیتزا!I9، gozaresh_naharkhoran · پیتزا!I10، gozaresh_naharkhoran · پیتزا!I11، gozaresh_naharkhoran · پیتزا!I13، gozaresh_naharkhoran · پیتزا!I15، gozaresh_naharkhoran · فرنگی!I6، gozaresh_naharkhoran · فرنگی!I7، gozaresh_naharkhoran · فرنگی!I8، gozaresh_naharkhoran · فرنگی!I9، gozaresh_naharkhoran · فرنگی!I10، gozaresh_naharkhoran · فرنگی!I11، gozaresh_naharkhoran · فرنگی!I12، gozaresh_naharkhoran · فرنگی!I13، gozaresh_naharkhoran · فرنگی!I14، gozaresh_naharkhoran · سوخاری!I6، gozaresh_naharkhoran · سوخاری!I7، gozaresh_naharkhoran · سوخاری!I8

```
function getTotalFoodsIngredient(foodIds, ingredientId, salesData, ingredientNamedRange,refresher="") {
  if(typeof foodIds === "number"){
    const foodValue = getFoodValueById(foodIds,salesData);
    const ingredientValue = getIngredientValue(foodIds, ingredientId, ingredientNamedRange);
    return foodValue * ingredientValue;
  }
  const arr = foodIds[0].map(foodId => {
    const foodValue = getFoodValueById(foodId,salesData);
    const ingredientValue = getIngredientValue(foodId, ingredientId, ingredientNamedRange);
    return foodValue * ingredientValue;
  });
 return arr.filter(x=>Boolean(x)).reduce((acc, currentValue) => acc + currentValue,0);
}
```

## getTotalFoodsIngredientForOneDay (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function getTotalFoodsIngredientForOneDay(foodIds, ingredientId, salesData, ingredientNamedRange, refresher = "") {
  if (getFoodValueById(foodIds[0], salesData) === "N/A") return "N/A";
  const arr = foodIds.map(foodId => {
    const foodValue = getFoodValueById(foodId, salesData);
    const ingredientValue = getIngredientValue(foodId, ingredientId, ingredientNamedRange);
    return typeof ingredientValue === "number" ? foodValue * ingredientValue : null
  });
  
  const filteredArr = arr.filter(v => v != undefined);
  const sum = filteredArr.reduce((acc, currentValue) => acc + currentValue);
  return sum;
}

**********************************************************************************
coefficients.gs:
```

## getTotalFoodsIngredientPerDay (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!F3، control_gozareshat · مواد حساس!G3، control_gozareshat · مواد حساس!J3، control_gozareshat · مواد حساس!F4، control_gozareshat · مواد حساس!G4، control_gozareshat · مواد حساس!J4، control_gozareshat · مواد حساس!F5، control_gozareshat · مواد حساس!G5، control_gozareshat · مواد حساس!J5، control_gozareshat · مواد حساس!F6، control_gozareshat · مواد حساس!G6، control_gozareshat · مواد حساس!J6، control_gozareshat · مواد حساس!F7، control_gozareshat · مواد حساس!G7، control_gozareshat · مواد حساس!J7، control_gozareshat · مواد حساس!F8، control_gozareshat · مواد حساس!G8، control_gozareshat · مواد حساس!J8، control_gozareshat · مواد حساس!F9، control_gozareshat · مواد حساس!G9

```
function getTotalFoodsIngredientPerDay(
  ingredientId,
  salesRows,
  ingredientNamedRange,
  refresher = "",
) {
  const foodIds = extractFoodIds(salesRows[0]);

  const x = salesRows.map((salesData, i) => {
    if (i !== 0) {
      return getTotalFoodsIngredientForOneDay(
        foodIds,
        ingredientId,
        [salesRows[0], salesData],
        ingredientNamedRange,
        refresher,
      );
    }
  });

  return x.filter(v => v != undefined)
}
```

## getTrendCoefficientLast3Days (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!G3، control_gozareshat · مواد حساس!G4، control_gozareshat · مواد حساس!G5، control_gozareshat · مواد حساس!G6، control_gozareshat · مواد حساس!G7، control_gozareshat · مواد حساس!G8، control_gozareshat · مواد حساس!G9، control_gozareshat · مواد حساس!G10، control_gozareshat · مواد حساس!G11، control_gozareshat · مواد حساس!G12، control_gozareshat · مواد حساس!G13، control_gozareshat · مواد حساس!G14، control_gozareshat · مواد حساس!G15، control_gozareshat · مواد حساس!G16، control_gozareshat · مواد حساس!G17، control_gozareshat · مواد حساس!G18، control_gozareshat · مواد حساس!G19، control_gozareshat · مواد حساس!G20، control_gozareshat · مواد حساس!G21، control_gozareshat · مواد حساس!G22

```
function getTrendCoefficientLast3Days(...days) {

  // ===== Configuration =====

  // Minimum percentage change required to detect a trend.
  // Example: 0.10 = 10%
  const TREND_THRESHOLD = 0.10;

  // Coefficient increase for an upward trend.
  // Example: 0.05 = +5%
  const ADJUST_UP = 0.05;

  // Coefficient decrease for a downward trend.
  // Example: 0.05 = -5%
  const ADJUST_DOWN = 0.05;

  // =========================
  const flatDays = days.map(day => Array.isArray(day) ? day.flat() : null).filter(v => Boolean(v));
  const [day1, day2, day3] = sumArrays(flatDays);
  const firstAverage = (day1 + day2) / 2;
  const lastAverage = (day2 + day3) / 2;

  if (firstAverage === 0) {
    return 1;
  }

  // Percentage change between the two averages
  const trend = (lastAverage - firstAverage) / firstAverage;

  if (trend >= TREND_THRESHOLD) {
    return 1 + ADJUST_UP;
  }

  if (trend <= -TREND_THRESHOLD) {
    return 1 - ADJUST_DOWN;
  }

  return 1;
}
```

## getValueById (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function getValueById(id, data, indicator = '#') {

  const headers = data[0];
  const foodIdString = indicator + id;

  let colIndex = -1;
  for (let i = 0; i < headers.length; i++) {
    if (headers[i].toString().includes(foodIdString)) {
      colIndex = i;
      break;
    }
  }

  if (colIndex === -1) {
    return "ID not found";
  }

  const rowData = data[1];
  const res = rowData[colIndex];
  return res === "" ? 0 : res;
}
```

## getValueById (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: —

```
function getValueById(id, data, indicator= '#') {

  const headers = data[0];
  const foodIdString = indicator + id; 
  
  let colIndex = -1;
  for (let i = 0; i < headers.length; i++) {
    if (headers[i].toString().includes(foodIdString)) {
      colIndex = i;
      break;
    }
  }

  if (colIndex === -1) {
    return "ID not found";
  }

  const rowData = data[1];
  return rowData[colIndex] === "#N/A" ? 0 : rowData[colIndex];
}
```

## getWeekDayCoefficient (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: control_gozareshat · مواد حساس!H3

```
function getWeekDayCoefficient(persianDate) {
  const weekDay = PERSIAN_WEEKDAY(persianDate);
  if (weekDay === "Wednesday") return 1.1;
  if (weekDay === "Thursday") return 1.2;
  if (weekDay === "Friday") return 1.15;
  return 1;
}
**********************************************************************************
utils.gs:
```

## gregorianToJalali (script)

تعریف‌شده در: Salon__Salon - Chalebagh/Salon - Chalebagh.gs، Sandogh__Sandogh - NaharKhoran/Sandogh - NaharKhoran.gs، Sandogh__Sandogh - Chalebagh/Sandogh - Chalebagh.gs

فراخوانی: —

```
function gregorianToJalali(gy, gm, gd) {
  var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  var jy = (gy <= 1600) ? 0 : 979;
  gy -= (gy <= 1600) ? 621 : 1600;
  var gy2 = (gm > 2) ? (gy + 1) : gy;
  var days = 365 * gy + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) +
             Math.floor((gy2 + 399) / 400) - 80 + gd + g_d_m[gm - 1];
  jy += 33 * Math.floor(days / 12053); days %= 12053;
  jy += 4 * Math.floor(days / 1461); days %= 1461;
  if (days > 365) {
    jy += Math.floor((days - 1) / 365);
    days = (days - 1) % 365;
  }
  var jm, jd;
  if (days < 186) {
    jm = 1 + Math.floor(days / 31);
    jd = 1 + (days % 31);
  } else {
    jm = 7 + Math.floor((days - 186) / 30);
    jd = 1 + ((days - 186) % 30);
  }
  return [jy, jm, jd];
}
```

## gregorianToPersianDate (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function gregorianToPersianDate(date) {
  const gy = date.getFullYear();
  const gm = date.getMonth() + 1;
  const gd = date.getDate();

  const g_d_m = [0,31,59,90,120,151,181,212,243,273,304,334];

  let jy;

  if (gy > 1600) {
    jy = 979;
  } else {
    jy = 0;
  }

  let gy2 = (gy > 1600) ? gy - 1600 : gy - 621;

  let days =
    (365 * gy2) +
    Math.floor((gy2 + 3) / 4) -
    Math.floor((gy2 + 99) / 100) +
    Math.floor((gy2 + 399) / 400) -
    80 +
    gd +
    g_d_m[gm - 1];

  if (gm > 2 && ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0))) {
    days++;
  }

  jy += 33 * Math.floor(days / 12053);
  days %= 12053;

  jy += 4 * Math.floor(days / 1461);
  days %= 1461;

  if (days > 365) {
    jy += Math.floor((days - 1) / 365);
    days = (days - 1) % 365;
  }

  let jm, jd;

  if (days < 186) {
    jm = 1 + Math.floor(days / 31);
    jd = 1 + (days % 31);
  } else {
    days -= 186;
    jm = 7 + Math.floor(days / 30);
    jd = 1 + (days % 30);
  }

  return (
    jy.toString().padStart(4, "0") +
    "/" +
    jm.toString().padStart(2, "0") +
    "/" +
    jd.toString().padStart(2, "0")
  );
}
```

## isValidPersianDate (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function isValidPersianDate(dateString) {
  return /^\d{4}\/\d{2}\/\d{2}$/.test(String(dateString));
}
```

## jalaliToGregorian (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: —

```
function jalaliToGregorian(jy, jm, jd) {
  var gy;
  var g_d_m, days;
  var sal_a = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  jy += 1595;
  var days = -355668 + (365 * jy) + Math.floor(jy / 33) * 8 + Math.floor(((jy % 33) + 3) / 4) + jd;

  for (var i = 1; i < jm; ++i)
    days += (i <= 6 ? 31 : 30);

  gy = 400 * Math.floor(days / 146097);
  days %= 146097;

  if (days > 36524) {
    gy += 100 * Math.floor(--days / 36524);
    days %= 36524;

    if (days >= 365)
      days++;
  }

  gy += 4 * Math.floor(days / 1461);
  days %= 1461;

  if (days > 365) {
    gy += Math.floor((days - 1) / 365);
    days = (days - 1) % 365;
  }

  var gd, gm;
  var leap = ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0));
  sal_a[2] = leap ? 29 : 28;

  for (gm = 1; gm <= 12 && days >= sal_a[gm]; gm++) {
    days -= sal_a[gm];
  }

  gd = days + 1;

  return new Date(gy, gm - 1, gd); // JS Date (month is 0-based)
}

**********************************************************************************
cumtomFunction.gs:
```

## logFormData (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function logFormData(formData,persianDateStr) {
  const categorizedFoodData = categorizeFoodData(formData,foodIdToCategory);
  updateFoodCount(persianDateStr, categorizedFoodData);
  return categorizedFoodData;
}

// Add a custom menu to open the form dialog
```

## onOpen (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: —

```
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Actions')
    .addItem('Recalculate All', 'triggerRecalculation')
    .addToUi();
}
```

## onOpen (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Actions')
    .addItem('محاسبه مجدد همه', 'triggerRecalculation')
    .addItem("ثبت سفارش", "showOrderDialog")
    .addToUi();
}
```

## onOpen (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Upload Sales Data')
    .addItem('Open Form', 'openFormDialog')
    .addToUi();
}
**********************************************************************************
foodIdToCategory.gs:


  const foodIdToCategory = {
    61: "italianPizza",
    62: "italianPizza",
    63: "italianPizza",
    310: "italianPizza",
    87: "italianPizza",
    73: "italianPizza",
    49: "italianPizza",
    551: "italianPizza",
    552: "italianPizza",
    13: "italianPizza",
    553: "italianPizza",
    768: "italianPizza",
    771: "italianPizza",
    71: "americanPizza",
    309: "americanPizza",
    74: "americanPizza",
    65: "americanPizza",
    76: "americanPizza",
    75: "americanPizza",
    308: "americanPizza",
    400: "americanPizza",
    27: "americanPizza",
    766: "americanPizza",
    767: "americanPizza",
    1: "americanPizza",
    4: "singlePizza",
    780: "singlePizza",
    783: "singlePizza",
    782: "singlePizza",
    781: "singlePizza",
    784: "singlePizza",
    86: "farangi",
    303: "farangi",
    82: "pasta",
    601: "pasta",
    85: "pasta",
    84: "pasta",
    131: "sandwich",
    133: "sandwich",
    134: "sandwich",
    132: "sandwich",
    138: "sandwich",
    139: "sandwich",
    136: "sandwich",
    151: "sandwich",
    137: "sandwich",
    44: "sandwich",
    150: "sandwich",
    773: "sandwich",
    769: "sandwich",
    401: "salad",
    402: "salad",
    407: "salad",
    385: "fried",
    120: "fried",
    386: "fried",
    350: "fried",
    122: "fried",
    123: "fried",
    5: "fried",
    81: "steak",
    360: "starter",
    11: "starter",
    27: "starter",
    7: "starter",
    504: "starter",
    101: "starter",
    110: "starter",
    277: "starter",
    273: "starter",
    368: "starter",
    102: "starter",
    104: "starter",
    108: "starter",
    112: "starter",
    358: "starter",
    374: "starter",
    110: "starter",
    752: "starter",
    754: "starter",
    757: "starter",
    338: "starter",
    348: "starter",
    10: "personel",
  };

**********************************************************************************
categorizeFoodData.gs:
```

## openFormDialog (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function openFormDialog() {
  const html = HtmlService.createHtmlOutputFromFile('uploadFileDialog')
      .setWidth(550)
      .setHeight(600);
  SpreadsheetApp.getUi().showModalDialog(html, 'Sales Data Form ');
}
```

## persianToGregorian (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function persianToGregorian(jy, jm, jd) {
  jy += 1595;
  var days = -355668 + (365 * jy) +
    (parseInt(jy / 33) * 8) +
    parseInt(((jy % 33) + 3) / 4) +
    jd +
    ((jm < 7) ? (jm - 1) * 31 : ((jm - 7) * 30) + 186);

  var gy = 400 * parseInt(days / 146097);
  days %= 146097;

  if (days > 36524) {
    gy += 100 * parseInt(--days / 36524);
    days %= 36524;
    if (days >= 365) days++;
  }

  gy += 4 * parseInt(days / 1461);
  days %= 1461;

  if (days > 365) {
    gy += parseInt((days - 1) / 365);
    days = (days - 1) % 365;
  }

  var gd = days + 1;
  var sal_a = [0, 31, ((gy % 4 == 0 && gy % 100 != 0) || (gy % 400 == 0)) ? 29 : 28,
    31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  var gm;
  for (gm = 1; gm <= 12 && gd > sal_a[gm]; gm++) {
    gd -= sal_a[gm];
  }

  return new Date(gy, gm - 1, gd);
}
```

## persianToGregorianDate (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function persianToGregorianDate(jdate) {

  if (Array.isArray(jdate)) {
    jdate = jdate[0][0];
  }

  const p = String(jdate).trim().split("/");

  if (p.length !== 3) {
    throw new Error("Invalid Persian date: " + jdate);
  }

  return persianToGregorian(
    parseInt(p[0], 10),
    parseInt(p[1], 10),
    parseInt(p[2], 10)
  );
}



**********************************************************************************
buffer.gs:
```

## saveOrders (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function saveOrders(selectedEvents){

  let coefficient=1;

  selectedEvents.forEach(key=>{
    if(EVENTS[key])
      coefficient*=EVENTS[key].factor;
  });

  const ss=SpreadsheetApp.getActive();

  const date=ss.getRangeByName("Date").getDisplayValue();

  const source=ss.getSheetByName(SOURCE_SHEET);
  const target=ss.getSheetByName(TARGET_SHEET);

  const headers=target.getRange(1,1,1,target.getLastColumn()).getValues()[0];

  const headerMap={};

  headers.forEach((h,i)=>{
    const m=String(h).match(/##(\d+)/);
    if(m)
      headerMap[m[1]]=i+1;
  });

  const row=new Array(headers.length).fill("");

  const dateCol=headers.indexOf("تاریخ");

  if(dateCol==-1)
    throw new Error("ستون تاریخ پیدا نشد.");

  row[dateCol]=date;

  const data=source.getRange(2,4,source.getLastRow()-1,8).getValues();

  data.forEach(r=>{

    const code=String(r[0]).trim();

    const amount=r[7];

    if(amount==="" || amount==null)
      return;

    const col=headerMap[code];

    if(!col)
      return;

    row[col-1]=Math.round(Number(amount)*coefficient);

  });

  target.appendRow(row);

  return "اطلاعات با موفقیت ثبت شد.";
}

**********************************************************************************
customeFuncs.gs:
```

## serialize (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function serialize(input) {
  return JSON.stringify(input, undefined, 1);
}
```

## showOrderDialog (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function showOrderDialog() {
  const html = HtmlService.createHtmlOutputFromFile("Dialog")
    .setWidth(700)
    .setHeight(500);

  SpreadsheetApp.getUi().showModalDialog(html, "ثبت سفارش");
}
```

## submitOrder (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function submitOrder(){

    if(!confirm("آیا سفارش ثبت شود؟"))
        return;

    google.script.run
        .withSuccessHandler(function(msg){

            alert(msg);
            google.script.host.close();

        })
        .saveOrders(selected);

}

  </script>

</body>

</html>

**********************************************************************************
```

## sumArrays (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function sumArrays(arrays) {
  if (arrays.length === 0) return [];
  return arrays[0].map((_, index) =>
    arrays.reduce((sum, arr) => sum + arr[index], 0)
  );
}
```

## sumArrays2 (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function sumArrays2(arrays) {
  if (arrays.length === 0) return [];
  return arrays.map(arr => {
    return arr.reduce((sum, current) => sum + current, 0);
  });
}
```

## triggerRecalculation (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function triggerRecalculation() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const triggerCell = sheet.getSheetByName('Refresher').getRange("A1");
  const date = new Date();
  triggerCell.setValue(date.getTime());
  SpreadsheetApp.flush();
}


const SOURCE_SHEET = "مواد حساس";
const TARGET_SHEET = "سفارشات ثبت شده";

const EVENTS = {
  tomorrowHoliday: {
    title: "تعطیلی روز آینده",
    factor: 1.10,
  },
  mourning: {
    title: "عزای عمومی",
    factor: 0.90,
  },
  ramadan: {
    title: "ماه رمضان",
    factor: 0.80,
  },
  competitorHoliday: {
    title: "تعطیلی رقیب اصلی",
    factor: 1.05,
  },
};
```

## triggerRecalculation (script)

تعریف‌شده در: MandeShab__Naharkhoran__Gozaresh naharkhoran/Gozaresh naharkhoran.gs، MandeShab__ChaleBagh__Gozaresh markazi/Gozaresh markazi.gs

فراخوانی: —

```
function triggerRecalculation() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const triggerCell = sheet.getSheetByName('Refresher').getRange("A1");
  const date = new Date();
  triggerCell.setValue(date.getTime());
  SpreadsheetApp.flush();
}

**********************************************************************************
date.gs:
```

## updateFoodCount (script)

تعریف‌شده در: MandeShab__Naharkhoran__Amar__Tedade Fooroosh naharkhoran/Tedade Fooroosh naharkhoran.gs، MandeShab__ChaleBagh__Amar__Tedade Fooroosh markazi/Tedade Fooroosh markazi.gs

فراخوانی: —

```
function updateFoodCount(persianDateStr,foodData) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  // Iterate over each category (sheet)

  for (const category in foodData) {
    const sheet = ss.getSheetByName(category);

    if (sheet) {
      const headers = sheet.getRange("1:1").getValues()[0];
      

      const newRow = [persianDateStr];


      const categoryData = foodData[category];
      headers.forEach((header, index) => {
        if(index === 0) return;
        const foodId = extractFoodIdFromHeader(header);


        if (foodId && categoryData[foodId] !== undefined) {
          newRow.push(categoryData[foodId]);
        } else {
          newRow.push(0);
        }
      });

      // Append the new row to the sheet
      sheet.appendRow(newRow);
    }
  }
}

// Helper function to extract foodId from the header (format "Food Name #foodId")
```

## updateSummary (script)

تعریف‌شده در: Gozareshat/Gozareshat.gs

فراخوانی: —

```
function updateSummary(){

    selected=[];

    let coefficient=1;

    let html="";

    document.querySelectorAll(".card.selected").forEach(card=>{

        selected.push(card.dataset.key);

        coefficient*=Number(card.dataset.factor);

        html+=`<div class="event">✓ ${card.dataset.title}</div>`;

    });

    if(html=="")
        html="بدون ضریب";

    document.getElementById("events").innerHTML=html;

    document.getElementById("factor").innerHTML="×"+coefficient.toFixed(3);

}
```
