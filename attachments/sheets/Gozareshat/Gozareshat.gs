**********************************************************************************
appscipt.json:
{
  "timeZone": "Asia/Tehran",
  "dependencies": {
  },
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8"
}
**********************************************************************************
Code.gs:


function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Actions')
    .addItem('محاسبه مجدد همه', 'triggerRecalculation')
    .addItem("ثبت سفارش", "showOrderDialog")
    .addToUi();
}

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



function showOrderDialog() {
  const html = HtmlService.createHtmlOutputFromFile("Dialog")
    .setWidth(700)
    .setHeight(500);

  SpreadsheetApp.getUi().showModalDialog(html, "ثبت سفارش");
}

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

function getFoodValueById(foodId, data, refresher = "") {
  return getValueById(foodId, data, '#')
}

function getIngredientValueById(ingredientId, data, refresher = "") {
  return getValueById(ingredientId, data, '##')
}

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


function getWeekDayCoefficient(persianDate) {
  const weekDay = PERSIAN_WEEKDAY(persianDate);
  if (weekDay === "Wednesday") return 1.1;
  if (weekDay === "Thursday") return 1.2;
  if (weekDay === "Friday") return 1.15;
  return 1;
}
**********************************************************************************
utils.gs:

function sumArrays2(arrays) {
  if (arrays.length === 0) return [];
  return arrays.map(arr => {
    return arr.reduce((sum, current) => sum + current, 0);
  });
}

function sumArrays(arrays) {
  if (arrays.length === 0) return [];
  return arrays[0].map((_, index) =>
    arrays.reduce((sum, arr) => sum + arr[index], 0)
  );
}

function serialize(input) {
  return JSON.stringify(input, undefined, 1);
}



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
function isValidPersianDate(dateString) {
  return /^\d{4}\/\d{2}\/\d{2}$/.test(String(dateString));
}

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

function PERSIAN_WEEKDAY(jdate) {
  var p = String(jdate).split("/");
  var g = persianToGregorian(Number(p[0]), Number(p[1]), Number(p[2]));

  return Utilities.formatDate(g, Session.getScriptTimeZone(), "EEEE");
}


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
