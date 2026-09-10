# Gozareshat

- spreadsheetId: `1ZDpoSy5EIzSUQ1bTEqIm-BS07q_CmbRaLDBgz3LgI-M`
- exported: 2026-08-29T10:38:50.643Z

## شیت‌ها

| # | نام | مخفی | ابعاد |
|---|---|---|---|
| 1 |  تاریخ | - | 8×8 |
| 2 | مواد حساس | - | 34×11 |
| 3 | مواد عادی | - | 79×11 |
| 4 | سفارشات ثبت شده | **بله** | 2×33 |
| 5 | Table_Ingredients_Pasta | **بله** | 3×6 |
| 6 | Table_Ingredients_Steak | **بله** | 2×3 |
| 7 | Table_Ingredients_Farangi | **بله** | 3×5 |
| 8 | Table_Ingredients_Starter | **بله** | 8×16 |
| 9 | Copy of مواد حساس | **بله** | 1012×26 |
| 10 | Refresher | **بله** | 1×1 |
| 11 | Table_Ingredients_Sandwich | **بله** | 14×14 |
| 12 | Table_Ingredients_Fried | **بله** | 8×11 |
| 13 | Table_Pizza_Last | **بله** | 160×15 |
| 14 | Table_Farangi_Last | **بله** | 161×18 |
| 15 | Table_KitchenCounter_Last | **بله** | 132×20 |
| 16 | Table_Fried_Last | **بله** | 127×11 |
| 17 | SheetsFileIDs | **بله** | 8×2 |
| 18 | Table_SalesData_AmericanPizza | **بله** | 187×13 |
| 19 | Table_SalesData_SinglePizza | **بله** | 48×7 |
| 20 | Table_SalesData_ItalianPizza | **بله** | 192×14 |
| 21 | Table_SalesData_Pasta | **بله** | 192×5 |
| 22 | Table_Ingredients_Lasagna | **بله** | 3×8 |
| 23 | Table_SalesData_Starter | **بله** | 192×22 |
| 24 | Table_SalesData_Personel | **بله** | 193×2 |
| 25 | Table_SalesData_Salad | **بله** | 192×4 |
| 26 | Table_SalesData_Fried | **بله** | 192×8 |
| 27 | Table_SalesData_Sandwich | **بله** | 192×12 |
| 28 | Table_SalesData_Farangi | **بله** | 192×3 |
| 29 | Table_SalesData_Steak | **بله** | 192×2 |
| 30 | Table_Ingredients_ItalianPizza | **بله** | 14×23 |
| 31 | Table_Ingredients_SinglePizza | **بله** | 7×19 |
| 32 | Table_Ingredients_AmericanPizza | **بله** | 13×18 |
| 33 | Table_Ingredients_Salad | **بله** | 4×9 |

## فرمول‌های یکتا

###  تاریخ

- `H2` ×1  →  `=FORMAT_PERSIAN_DATE(C5,D5,E5)`

### مواد حساس

- `F3` ×1  →  `=LET(
ingredientId, D3,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
friedSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
average, getAverage({friTotal, stTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G3` ×2  →  `=LET(
ingredientId, D3,
starterSalesData,getLast3DaysRows(Table_SalesData_Starter,Date),
friedSalesData,getLast3DaysRows(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getTrendCoefficientLast3Days(friTotal, stTotal)
)`
- `H3` ×1  →  `=getWeekDayCoefficient(Date)`
- `I3` ×2  →  `=LET(
farangiData, getPreviousDayRow(Table_KitchenCounter_Last,Date),
totalGr, getIngredientValueById(D3,farangiData,Refresher),
CONVERT_GR_TO_KG(totalGr)
)`
- `J3` ×1  →  `=LET(
ingredientId, D3,
starterSalesData,getPreviousDayRow(Table_SalesData_Starter,Date),
friedSalesData,getPreviousDayRow(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sum, SUM(friTotal, stTotal),
calcBuffer(F3,CONVERT_GR_TO_KG(sum))
)`
- `K3` ×32  →  `=(((F3*G3)*H3)+J3)-I3`
- `F4` ×1  →  `=LET(
ingredientId, D4,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
friedSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getAverage({friTotal, stTotal})
)`
- `H4` ×31  →  `=H3`
- `I4` ×1  →  `=LET(
farangiData, getPreviousDayRow(Table_KitchenCounter_Last,Date),
getIngredientValueById(D4,farangiData,Refresher)
)`
- `J4` ×1  →  `=LET(
ingredientId, D4,
starterSalesData,getPreviousDayRow(Table_SalesData_Starter,Date),
friedSalesData,getPreviousDayRow(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sum, SUM(friTotal, stTotal),
calcBuffer(F4,sum)
)`
- `F5` ×1  →  `=LET(
ingredientId, D5,
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
paTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
average, getAverage({amTotal, itTotal, sinTotal, paTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G5` ×1  →  `=LET(
ingredientId, D5,
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
paTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
getTrendCoefficientLast3Days(amTotal, itTotal, sinTotal, paTotal)
)`
- `J5` ×1  →  `=LET(
ingredientId, D5,
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
paTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
sum, SUM(amTotal, itTotal, sinTotal, paTotal),
calcBuffer(F5,CONVERT_GR_TO_KG(sum))
)`
- `F6` ×4  →  `=LET(
ingredientId, D6,
sandwichSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getAverage({sanTotal})
)`
- `G6` ×4  →  `=LET(
ingredientId, D6,
sandwichSalesData,getLast3DaysRows(Table_SalesData_Sandwich,Date),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getTrendCoefficientLast3Days(sanTotal)
)`
- `I6` ×7  →  `=LET(
farangiData, getPreviousDayRow(Table_Farangi_Last,Date),
getIngredientValueById(D6,farangiData,Refresher)
)`
- `J6` ×4  →  `=LET(
ingredientId, D6,
sandwichSalesData,getPreviousDayRow(Table_SalesData_Sandwich,Date),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
sum, SUM(sanTotal),
calcBuffer(F6,sum)
)`
- `F7` ×2  →  `=LET(
ingredientId, D7,
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getAverage({itTotal})
)`
- `G7` ×4  →  `=LET(
ingredientId, D7,
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getTrendCoefficientLast3Days(itTotal)
)`
- `J7` ×2  →  `=LET(
ingredientId, D7,
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sum, SUM(itTotal),
calcBuffer(F7,sum))`
- `F8` ×1  →  `=LET(
ingredientId, D8,
frangiSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Farangi,Date),
sandwichSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
average, getAverage({fraTotal,sanTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G8` ×1  →  `=LET(
ingredientId, D8,
frangiSalesData,getLast3DaysRows(Table_SalesData_Farangi,Date),
sandwichSalesData,getLast3DaysRows(Table_SalesData_Sandwich,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getTrendCoefficientLast3Days(fraTotal,sanTotal)
)`
- `I8` ×6  →  `=LET(
farangiData, getPreviousDayRow(Table_Farangi_Last,Date),
totalGr, getIngredientValueById(D8,farangiData,Refresher),
CONVERT_GR_TO_KG(totalGr)
)`
- `J8` ×1  →  `=LET(
ingredientId, D8,
frangiSalesData,getPreviousDayRow(Table_SalesData_Farangi,Date),
sandwichSalesData,getPreviousDayRow(Table_SalesData_Sandwich,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
sum, SUM(fraTotal,sanTotal),
calcBuffer(F8,CONVERT_GR_TO_KG(sum))
)`
- `F9` ×1  →  `=LET(
ingredientId, D9,

frangiSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Farangi,Date),
sandwichSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
saladSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Salad,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
steakSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Steak,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
average, getAverage({saTotal, paTotal, fraTotal, sanTotal, steakTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G9` ×1  →  `=LET(
ingredientId, D9,

frangiSalesData,getLast3DaysRows(Table_SalesData_Farangi,Date),
sandwichSalesData,getLast3DaysRows(Table_SalesData_Sandwich,Date),
saladSalesData,getLast3DaysRows(Table_SalesData_Salad,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
steakSalesData,getLast3DaysRows(Table_SalesData_Steak,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
getTrendCoefficientLast3Days(saTotal, paTotal, fraTotal, sanTotal, steakTotal)
)`
- `J9` ×1  →  `=LET(
ingredientId, D9,

frangiSalesData,getPreviousDayRow(Table_SalesData_Farangi,Date),
sandwichSalesData,getPreviousDayRow(Table_SalesData_Sandwich,Date),
saladSalesData,getPreviousDayRow(Table_SalesData_Salad,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
steakSalesData,getPreviousDayRow(Table_SalesData_Steak,Date),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
sum, SUM(saTotal, paTotal, fraTotal, sanTotal, steakTotal),
calcBuffer(F9,CONVERT_GR_TO_KG(sum))
)`
- `F10` ×1  →  `=LET(
ingredientId, D10,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
average, getAverage({stTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G10` ×1  →  `=LET(
ingredientId, D10,
starterSalesData,getLast3DaysRows(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getTrendCoefficientLast3Days(stTotal)
)`
- `J10` ×1  →  `=LET(
ingredientId, D10,
starterSalesData,getPreviousDayRow(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sum, SUM(stTotal),
calcBuffer(F10,CONVERT_GR_TO_KG(sum))
)`
- `F12` ×1  →  `=LET(
ingredientId, D12,
saladSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Salad,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
average, getAverage({saTotal, paTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G12` ×1  →  `=LET(
ingredientId, D12,
saladSalesData,getLast3DaysRows(Table_SalesData_Salad,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
getTrendCoefficientLast3Days(saTotal, paTotal)
)`
- `J12` ×1  →  `=LET(
ingredientId, D12,
saladSalesData,getPreviousDayRow(Table_SalesData_Salad,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
sum, SUM(saTotal, paTotal),
calcBuffer(F12,CONVERT_GR_TO_KG(sum))
)`
- `F13` ×1  →  `=LET(
ingredientId, D13,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
frangiSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Farangi,Date),
sandwichSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
average, getAverage({paTotal, fraTotal, sanTotal, stTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G13` ×1  →  `=LET(
ingredientId, D13,
starterSalesData,getLast3DaysRows(Table_SalesData_Starter,Date),
frangiSalesData,getLast3DaysRows(Table_SalesData_Farangi,Date),
sandwichSalesData,getLast3DaysRows(Table_SalesData_Sandwich,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
getTrendCoefficientLast3Days(paTotal, fraTotal, sanTotal, stTotal)
)`
- `J13` ×1  →  `=LET(
ingredientId, D13,
starterSalesData,getPreviousDayRow(Table_SalesData_Starter,Date),
frangiSalesData,getPreviousDayRow(Table_SalesData_Farangi,Date),
sandwichSalesData,getPreviousDayRow(Table_SalesData_Sandwich,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
fraTotal,getTotalFoodsIngredientPerDay(ingredientId,frangiSalesData,"Table_Ingredients_Farangi",Refresher),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
sum, SUM(paTotal, fraTotal, sanTotal, stTotal),
calcBuffer(F13,CONVERT_GR_TO_KG(sum)))`
- `F17` ×1  →  `=LET(
ingredientId, D17,
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
average, getAverage({paTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G17` ×1  →  `=LET(
ingredientId, D17,
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
getTrendCoefficientLast3Days(paTotal)
)`
- `J17` ×1  →  `=LET(
ingredientId, D17,
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
paTotal, getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Pasta",Refresher),
sum, SUM(paTotal),
calcBuffer(F17,CONVERT_GR_TO_KG(sum))
)`
- `F18` ×1  →  `=LET(
ingredientId, D18,
steakSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Steak,Date),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
getAverage({steakTotal})
)`
- `G18` ×1  →  `=LET(
ingredientId, D18,
steakSalesData,getLast3DaysRows(Table_SalesData_Steak,Date),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
getTrendCoefficientLast3Days(steakTotal)
)`
- `J18` ×1  →  `=LET(
ingredientId, D18,
steakSalesData,getPreviousDayRow(Table_SalesData_Steak,Date),
steakTotal, getTotalFoodsIngredientPerDay(ingredientId,steakSalesData,"Table_Ingredients_Steak",Refresher),
calcBuffer(F9,steakTotal)
)`
- `F19` ×2  →  `=LET(
ingredientId, D19,
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
average, getAverage({amTotal,itTotal,laTotal,sinTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G19` ×2  →  `=LET(
ingredientId, D19,
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
getTrendCoefficientLast3Days(amTotal,itTotal,laTotal,sinTotal)
)`
- `I19` ×10  →  `=LET(
farangiData, getPreviousDayRow(Table_Pizza_Last,Date),
totalGr, getIngredientValueById(D19,farangiData,Refresher),
CONVERT_GR_TO_KG(totalGr)
)`
- `J19` ×2  →  `=LET(
ingredientId, D19,
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
sum, SUM(amTotal,itTotal,laTotal,sinTotal),
calcBuffer(F19,CONVERT_GR_TO_KG(sum))
)`
- `F21` ×2  →  `=LET(
ingredientId, D21,
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
average, getAverage({itTotal}),
CONVERT_GR_TO_KG(average)
)`
- `J21` ×2  →  `=LET(
ingredientId, D21,
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sum, SUM(itTotal),
calcBuffer(F21,CONVERT_GR_TO_KG(sum)))`
- `F22` ×3  →  `=LET(
ingredientId, D22,
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
average, getAverage({amTotal,itTotal,sinTotal}),
CONVERT_GR_TO_KG(average))`
- `G22` ×3  →  `=LET(
ingredientId, D22,
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getTrendCoefficientLast3Days(amTotal,itTotal,sinTotal))`
- `J22` ×3  →  `=LET(
ingredientId, D22,
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sum, SUM(amTotal,itTotal,sinTotal),
calcBuffer(F22,CONVERT_GR_TO_KG(sum))
)`
- `F26` ×1  →  `=LET(
ingredientId, D26,
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
average, getAverage({amTotal,itTotal,sinTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G26` ×1  →  `=LET(
ingredientId, D26,
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getTrendCoefficientLast3Days(amTotal,itTotal,sinTotal)
)`
- `J26` ×1  →  `=LET(
ingredientId, D26,
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sum, SUM(amTotal,itTotal,sinTotal),
calcBuffer(F26,CONVERT_GR_TO_KG(sum))
)`
- `F27` ×1  →  `=LET(
ingredientId, D27,
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Pasta,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
average, getAverage({amTotal,itTotal,laTotal,sinTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G27` ×1  →  `=LET(
ingredientId, D27,
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getLast3DaysRows(Table_SalesData_Pasta,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
getTrendCoefficientLast3Days(amTotal,itTotal,laTotal,sinTotal)
)`
- `J27` ×1  →  `=LET(
ingredientId, D27,
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
pastaSalesData,getPreviousDayRow(Table_SalesData_Pasta,Date),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
laTotal,getTotalFoodsIngredientPerDay(ingredientId,pastaSalesData,"Table_Ingredients_Lasagna",Refresher),
sum, SUM(amTotal,itTotal,laTotal,sinTotal),
calcBuffer(F27,CONVERT_GR_TO_KG(sum))
)`
- `F28` ×1  →  `=LET(
ingredientId, D28,
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
starterSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
average, getAverage({amTotal,itTotal,sinTotal,stTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G28` ×1  →  `=LET(
ingredientId, D28,
singlePizzaSalesData,getLast3DaysRows(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getLast3DaysRows(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getLast3DaysRows(Table_SalesData_ItalianPizza,Date),
starterSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getTrendCoefficientLast3Days(amTotal,itTotal,sinTotal,stTotal)
)`
- `J28` ×1  →  `=LET(
ingredientId, D28,
singlePizzaSalesData,getPreviousDayRow(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getPreviousDayRow(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getPreviousDayRow(Table_SalesData_ItalianPizza,Date),
starterSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
sum, SUM(amTotal,itTotal,sinTotal,stTotal),
calcBuffer(F28,CONVERT_GR_TO_KG(sum))
)`
- `F29` ×2  →  `=LET(
ingredientId, D29,
friedSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
sandwichSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
frTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
sanTotal, getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getAverage({frTotal,sanTotal})
)`
- `G29` ×2  →  `=LET(
ingredientId, D29,
friedSalesData, getLast3DaysRows(Table_SalesData_Fried,Date),
sandwichSalesData, getLast3DaysRows(Table_SalesData_Sandwich,Date),
frTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
sanTotal, getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getTrendCoefficientLast3Days({frTotal,sanTotal})
)`
- `I29` ×5  →  `=LET(
farangiData, getPreviousDayRow(Table_Fried_Last,Date),
getIngredientValueById(D29,farangiData,Refresher)
)`
- `J29` ×2  →  `=LET(
ingredientId, D29,
friedSalesData, getPreviousDayRow(Table_SalesData_Fried,Date),
sandwichSalesData, getPreviousDayRow(Table_SalesData_Sandwich,Date),
frTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
sanTotal, getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
sum, SUM(frTotal,sanTotal),
calcBuffer(F29,sum)
)`
- `F31` ×2  →  `=LET(
ingredientId, D31,
saladSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Salad,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
getAverage({saTotal})
)`
- `G31` ×2  →  `=LET(
ingredientId, D31,

saladSalesData, getLast3DaysRows(Table_SalesData_Salad,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
getTrendCoefficientLast3Days({saTotal})
)`
- `J31` ×2  →  `=LET(
ingredientId, D31,
saladSalesData, getPreviousDayRow(Table_SalesData_Salad,Date),
saTotal, getTotalFoodsIngredientPerDay(ingredientId,saladSalesData,"Table_Ingredients_Salad",Refresher),
sum, SUM(saTotal),
calcBuffer(F31,sum)
)`
- `F33` ×1  →  `=LET(
ingredientId, D33,
starterSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getAverage({stTotal})
)`
- `G33` ×1  →  `=LET(
ingredientId, D33,
starterSalesData, getLast3DaysRows(Table_SalesData_Starter,Date),
total,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getTrendCoefficientLast3Days({total})
)`
- `J33` ×1  →  `=LET(
ingredientId, D33,
starterSalesData, getPreviousDayRow(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sum, SUM(stTotal),
calcBuffer(F33,sum)
)`
- `F34` ×1  →  `=LET(
ingredientId, D34,
starterSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
friedSalesData, getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
stTotal, getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
friTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
average,getAverage({stTotal,friTotal}),
CONVERT_GR_TO_KG(average)
)`
- `G34` ×1  →  `=LET(
ingredientId, D34,
starterSalesData, getLast3DaysRows(Table_SalesData_Starter,Date),
friedSalesData, getLast3DaysRows(Table_SalesData_Fried,Date),

stTotal, getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
friTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
getTrendCoefficientLast3Days({stTotal,friTotal})
)`
- `I34` ×1  →  `=LET(
farangiData, getPreviousDayRow(Table_Fried_Last,Date),
totalGr, getIngredientValueById(D34,farangiData,Refresher),
CONVERT_GR_TO_KG(totalGr)
)`
- `J34` ×1  →  `=LET(
ingredientId, D34,
starterSalesData, getPreviousDayRow(Table_SalesData_Starter,Date),
friedSalesData, getPreviousDayRow(Table_SalesData_Fried,Date),
stTotal, getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
friTotal, getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
sum, SUM(stTotal,friTotal),
calcBuffer(F34,CONVERT_GR_TO_KG(sum))
)`

### مواد عادی

- `F3` ×3  →  `=LET(
ingredientId, D3,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
friedSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getAverage({friTotal, stTotal})
)`
- `F5` ×2  →  `=LET(
ingredientId, D5,
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getAverage({itTotal})
)`
- `F6` ×1  →  `=LET(
ingredientId, D6,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
getAverage({amTotal,stTotal})
)`
- `F14` ×1  →  `=LET(
ingredientId, D14,
singlePizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_SinglePizza,Date),
americanPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,Date),
italianPizzaSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_ItalianPizza,Date),
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
sinTotal,getTotalFoodsIngredientPerDay(ingredientId,singlePizzaSalesData,"Table_Ingredients_SinglePizza",Refresher),
amTotal,getTotalFoodsIngredientPerDay(ingredientId,americanPizzaSalesData,"Table_Ingredients_AmericanPizza",Refresher),
itTotal,getTotalFoodsIngredientPerDay(ingredientId,italianPizzaSalesData,"Table_Ingredients_ItalianPizza",Refresher),
getAverage({amTotal,itTotal,sinTotal,stTotal})
)`
- `F30` ×2  →  `=LET(
ingredientId, D30,
sandwichSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Sandwich,Date),
sanTotal,getTotalFoodsIngredientPerDay(ingredientId,sandwichSalesData,"Table_Ingredients_Sandwich",Refresher),
getAverage({sanTotal})
)`
- `D32` ×14  →  `=AI("fill with constant numbers started from 71 and increase by one for each row")`
- `F35` ×1  →  `=LET(
ingredientId, D35,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getAverage({stTotal})
)`
- `C79` ×1  →  `=LET(
ingredientId, D3,
starterSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Starter,Date),
friedSalesData,getSameWeekdayRowsLast30Days(Table_SalesData_Fried,Date),
friTotal,getTotalFoodsIngredientPerDay(ingredientId,friedSalesData,"Table_Ingredients_Fried",Refresher),
stTotal,getTotalFoodsIngredientPerDay(ingredientId,starterSalesData,"Table_Ingredients_Starter",Refresher),
getAverage2({friTotal,stTotal})
)`

### Table_Ingredients_Pasta _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "پاستا",
dataRange,"A:N",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_Steak _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "استیک",
dataRange,"A:F",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_Farangi _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "فرنگی",
dataRange,"A:G",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_Starter _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "استارتر",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Copy of مواد حساس _(مخفی)_

- `J3` ×1  →  `=PERSIAN_WEEKDAY(H1)`
- `N4` ×1  →  `=AVERAGE(
  FILTER(
    INDEX(
      Table_SalesData_AmericanPizza,,
      MATCH(H2, INDEX(Table_SalesData_AmericanPizza,1,),0)
    ),

    ARRAYFORMULA(
      PERSIAN_WEEKDAY(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) = PERSIAN_WEEKDAY(H1),

    ARRAYFORMULA(
      PERSIAN_TO_GREGORIAN(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) >= PERSIAN_TO_GREGORIAN(H1)-30,

    ARRAYFORMULA(
      PERSIAN_TO_GREGORIAN(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) <= PERSIAN_TO_GREGORIAN(H1)
  )
)`
- `J5` ×1  →  `=AVERAGE(
  FILTER(
    INDEX(Table_SalesData_AmericanPizza,,2),
    
    ARRAYFORMULA(
      PERSIAN_WEEKDAY(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) = PERSIAN_WEEKDAY(H1),

    ARRAYFORMULA(
      PERSIAN_TO_GREGORIAN(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) >= PERSIAN_TO_GREGORIAN(H1)-30,

    ARRAYFORMULA(
      PERSIAN_TO_GREGORIAN(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    ) <= PERSIAN_TO_GREGORIAN(H1)
  )
)`
- `J9` ×1  →  `=AVERAGE(
  FILTER(
    Table_SalesData_AmericanPizza,
   
      PERSIAN_WEEKDAY(
        INDEX(Table_SalesData_AmericanPizza,,1)
      )
    = PERSIAN_WEEKDAY(TEXT(H1))
  )
)`
- `N9` ×1  →  `= getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,H1)`
- `H13` ×1  →  `=MAP(
  INDEX(Table_SalesData_AmericanPizza,,1),
  LAMBDA(d, PERSIAN_WEEKDAY(d))
)`
- `L15` ×1  →  `= H1 >L13`
- `N16` ×1  →  `=LET(
amFoodIds,{71, 309, 74, 65, 76, 75, 308, 400, 27, 766, 767},
ingredientId,1,
salesRows,getSameWeekdayRowsLast30Days(Table_SalesData_AmericanPizza,H1),
getTotalFoodsIngredientLast30Days(amFoodIds,ingredientId,salesRows,"Table_Ingredients_AmericanPizza",Refresher)
)`

### Table_Ingredients_Sandwich _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "ساندویچ",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_Fried _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "سوخاری",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Pizza_Last _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "موجودی آخر شب",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Pizza,sheetName,dataRange)
)`

### Table_Farangi_Last _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "موجودی آخر شب",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Farangi,sheetName,dataRange)
)`

### Table_KitchenCounter_Last _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "موجودی آخر شب",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_KitchenCounter,sheetName,dataRange)
)`

### Table_Fried_Last _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "موجودی آخر شب",
dataRange,"A:S",
IMPORT_FROM_SHEET(SheetsFileId_Fried,sheetName,dataRange)
)`

### Table_SalesData_AmericanPizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "americanPizza",
dataRange,"A:M",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_SinglePizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "singlePizza",
dataRange,"A:M",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_ItalianPizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "italianPizza",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Pasta _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "pasta",
dataRange,"A:E",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_Ingredients_Lasagna _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "لازانیا",
dataRange,"A:K",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_SalesData_Starter _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "starter",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Personel _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "personel",
dataRange,"A:B",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Salad _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "salad",
dataRange,"A:D",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Fried _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "fried",
dataRange,"A:H",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Sandwich _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "sandwich",
dataRange,"A:L",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Farangi _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "farangi",
dataRange,"A:C",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_SalesData_Steak _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "steak",
dataRange,"A:C",
IMPORT_FROM_SHEET(SheetsFileId_SalesData,sheetName,dataRange)
)`

### Table_Ingredients_ItalianPizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "پیتزا ایتالیایی",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_SinglePizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "پیتزا سینگل",
dataRange,"A:X",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_AmericanPizza _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "پیتزا امریکایی",
dataRange,"A:R",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`

### Table_Ingredients_Salad _(مخفی)_

- `A1` ×1  →  `=LET(
sheetName, "سالاد",
dataRange,"A:R",
IMPORT_FROM_SHEET(SheetsFileId_Ingredients,sheetName,dataRange)
)`


## توابع استفاده‌شده

ARRAYFORMULA, AVERAGE, CONVERT_GR_TO_KG, FILTER, FORMAT_PERSIAN_DATE, IMPORT_FROM_SHEET, INDEX, LAMBDA, LET, MAP, MATCH, PERSIAN_TO_GREGORIAN, PERSIAN_WEEKDAY, SUM, TEXT

## محتوای کامل: SheetsFileIDs

```
Range Name Associated	Sheets File Id
SheetsFileId_SalesData	1AIjH-sWVc6t5bXnEKiYrmrpX1TPtEbKtwZA0tjr-5bI
SheetsFileId_Farangi	1M_iuhWUW9901F_66pv_g8r0W0QVMzLDrEQJp6GQgnuQ
SheetsFileId_KitchenCounter	19jHmcKHJm8aOOef8kuiTRuGrswmUs4TKDaM1aAchwRk
SheetsFileId_Pizza	1dmH8tCqOuqNr2nt4AwJrHC2cq-rv0tIBHc4kk05bWtU
SheetsFileId_Fried	1Xy-f9VYXMlPLyibBsEh_oUHSOqjxXou1CJdOG4CPtbQ
SheetsFileId_Ingredients	15M2ovUmBvK3AMzGxeq-ijwE_KOQBjOZakLvQCs-eE10
SheetsFileId_Warehouse	1crVTmnxyXx4w_mwr0kJKsv8f_P0xKmuEj1YAEok6FkE
```
