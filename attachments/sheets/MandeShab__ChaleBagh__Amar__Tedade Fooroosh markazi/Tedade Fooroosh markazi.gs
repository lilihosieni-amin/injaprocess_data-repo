**********************************************************************************
Code.js:
// This function opens the form dialog
function openFormDialog() {
  const html = HtmlService.createHtmlOutputFromFile('uploadFileDialog')
      .setWidth(550)
      .setHeight(600);
  SpreadsheetApp.getUi().showModalDialog(html, 'Sales Data Form ');
}

function logFormData(formData,persianDateStr) {
  const categorizedFoodData = categorizeFoodData(formData,foodIdToCategory);
  updateFoodCount(persianDateStr, categorizedFoodData);
  return categorizedFoodData;
}

// Add a custom menu to open the form dialog
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
