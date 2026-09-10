Code.gs:function gregorianToJalali(gy, gm, gd) {
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

function GREG_TO_JALALI(dateInput) {
  if(!dateInput) return "";
  if (!(dateInput instanceof Date)) return "Invalid date";

  const gy = dateInput.getFullYear();
  const gm = dateInput.getMonth() + 1; // JavaScript months are 0-based
  const gd = dateInput.getDate();

  const [jy, jm, jd] = gregorianToJalali(gy, gm, gd);
  return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;
}

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

function GET_JALALI_YEAR(jalaliDateString) {
  if(!jalaliDateString) return '';
  if (!/^1[34]\d{2}\/\d{1,2}\/\d{1,2}$/.test(jalaliDateString)) {
    return "Invalid date format";
  }

  const parts = jalaliDateString.split("/");
  return parseInt(parts[0], 10);
}



