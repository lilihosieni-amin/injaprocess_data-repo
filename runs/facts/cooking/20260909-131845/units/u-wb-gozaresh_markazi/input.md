# u-wb-gozaresh_markazi

نوع: workbook — 16 نامزد تصمیم

## نامزدها

S-gs-94fd545e6e24 · «triggerRecalculation» · 1 variant · 0 bindings · params: —
    
S-gs-c02f6e7d98e9 · «triggerRecalculation» · 1 variant · 0 bindings · params: —
    
S-r-03cc0b0a549b · «موجودی آخر شب» · 5 variant · 60 bindings · params: p1، p2، p3، p4، ref_1، ref_2، ref_3، table_1
    ref_1 → «پیتزا» ستون b «—»
    ref_2 → CN
    ref_3 → DN
    table_1 → Table_Pizza_Last
    p1 → 5
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v2,getIngredientValueById(#,v1,Refresher),CONVERT_GR_TO_KG(v2))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getIngredientValueById(#,v1,Refresher))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
S-r-2290f11e1731 · «انحراف» · 1 variant · 8 bindings · params: ref_1، ref_2
    ref_1 → «پیتزا» ستون i «مصرف واقعی»
    ref_2 → «پیتزا» ستون h «مصرف اعلامی»
    MINUS(@,@)
S-r-23eed1eb390c · «موجودی اول شب» · 5 variant · 60 bindings · params: p1، p2، p3، p4، ref_1، ref_2، ref_3، table_1
    ref_1 → «پیتزا» ستون b «—»
    ref_2 → CN
    ref_3 → DN
    table_1 → Table_Pizza_First
    p1 → 5
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v2,getIngredientValueById(#,v1,Refresher),CONVERT_GR_TO_KG(v2))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getIngredientValueById(#,v1,Refresher))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
S-r-528d396c09d4 · «مصرف اعلامی» · 1 variant · 8 bindings · params: ref_1، ref_2، ref_3
    ref_1 → «پیتزا» ستون f «مقدار دریافت از انبار»
    ref_2 → «پیتزا» ستون e «موجودی اول شب»
    ref_3 → «پیتزا» ستون g «موجودی آخر شب»
    MINUS(SUM(@,@),@)
S-r-7317c7a8ece3 · «تعداد فروش» · 12 variant · 38 bindings · params: amFoodIds، fraFoodIds، itFoodIds، laFoodIds، p1، p2، p3، p4، paFoodIds، ref_1، ref_10، ref_11، ref_12، ref_13، ref_14، ref_15، ref_16، ref_17، ref_18، ref_2، ref_3، ref_4، ref_5، ref_6، ref_7، ref_8، ref_9، saFoodIds، sanFoodIds، sinFoodIds، stFoodIds، steakFoodIds، table_1، table_2، table_3، table_4، table_5، table_6
    amFoodIds → [74, 65, 76]
    itFoodIds → [63, 73, 49, 553]
    sinFoodIds → 783
    ref_1 → «پیتزا» ستون b «—»
    ref_2 → CN
    ref_3 → DN
    table_1 → Table_SalesData_SinglePizza
    ref_4 → «پیتزا» ستون b «—»
    ref_5 → CN
    ref_6 → DN
    table_2 → Table_SalesData_AmericanPizza
    ref_7 → «پیتزا» ستون b «—»
    ref_8 → CN
    ref_9 → DN
    table_3 → Table_SalesData_ItalianPizza
    LET(v1,{#},v2,{#},v3,{#},v4,{#},v5,{#},v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v9,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v10,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v11,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v12,getTotalFoodsCountsInRowById(v1,v6,Refresher),v13,getTotalFoodsCountsInRowById(v2,v7,Refresher),v14,getTotalFoodsCountsInRowById(v3,v8,Refresher),v15,getTotalFoodsCountsInRowById(v4,v9,Refresher),v16,getTotalFoodsCountsInRowById(v5,v10,Refresher),v17,getTotalFoodsCountsInRowById(#,v11,Refresher),SUM(v12,v13,v14,v15,v16,v17))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v2,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v3,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,getTotalFoodsCountsInRowById(#,v4,Refresher),v6,getTotalFoodsCountsInRowById(#,v1,Refresher),v7,getTotalFoodsCountsInRowById(#,v2,Refresher),v8,getTotalFoodsCountsInRowById(#,v3,Refresher),SUM(v6,v7,v8,v5))
    LET(v1,{#},v2,{#},v3,#,v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,getTotalFoodsCountsInRowById(v3,v7,Refresher),v9,getTotalFoodsCountsInRowById(v1,v4,Refresher),v10,getTotalFoodsCountsInRowById(v2,v5,Refresher),v11,getTotalFoodsCountsInRowById(#,v6,Refresher),SUM(v9,v10,v11,v8))
    LET(v1,{#},v2,{#},v3,#,v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,getTotalFoodsCountsInRowById(v3,v4,Refresher),v8,getTotalFoodsCountsInRowById(v1,v5,Refresher),v9,getTotalFoodsCountsInRowById(v2,v6,Refresher),SUM(v8,v9,v7))
    LET(v1,{#},v2,{#},v3,#,v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,getTotalFoodsCountsInRowById(v3,v4,Refresher),v9,getTotalFoodsCountsInRowById(v1,v5,Refresher),v10,getTotalFoodsCountsInRowById(v2,v6,Refresher),v11,getTotalFoodsCountsInRowById(#,v7,Refresher),SUM(v9,v10,v11,v8))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getTotalFoodsCountsInRowById(#,v1,Refresher))
    LET(v1,{#},v2,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getTotalFoodsCountsInRowById(v1,v2,Refresher))
    LET(v1,{#},v2,{#},v3,{#},v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,getTotalFoodsCountsInRowById(v3,v4,Refresher),v8,getTotalFoodsCountsInRowById(v1,v5,Refresher),v9,getTotalFoodsCountsInRowById(v2,v6,Refresher),SUM(v8,v9,v7))
    LET(v1,#,v2,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getTotalFoodsCountsInRowById(v1,v2,Refresher))
    LET(v1,#,v2,#,v3,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,getTotalFoodsCountsInRowById(v1,v3,Refresher),v6,getTotalFoodsCountsInRowById(v2,v4,Refresher),SUM(v5,v6))
    LET(v1,{#},v2,{#},v3,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,getTotalFoodsCountsInRowById(v1,v3,Refresher),v6,getTotalFoodsCountsInRowById(v2,v4,Refresher),SUM(v5,v6))
    LET(v1,#,v2,{#},v3,#,v4,#,v5,#,v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v9,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v10,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v11,getTotalFoodsCountsInRowById(v1,v6,Refresher),v12,getTotalFoodsCountsInRowById(v2,v7,Refresher),v13,getTotalFoodsCountsInRowById(v3,v8,Refresher),v14,getTotalFoodsCountsInRowById(v4,v9,Refresher),v15,getTotalFoodsCountsInRowById(v5,v10,Refresher),SUM(v11,v12,v13,v14,v15))
S-r-81679c88d37b · «انحراف به ازای هر عدد (با تلورانس)» · 2 variant · 3 bindings · params: p1، ref_1، ref_2
    ref_1 → «پیتزا» ستون l «انحراف (با تلورانس)»
    ref_2 → «پیتزا» ستون k «تعداد فروش»
    p1 → 3
    ROUND(DIVIDE(@,@),#)
    DIVIDE(@,@)
S-r-821dcf50a715 · «انحراف (با تلورانس)» · 2 variant · 10 bindings · params: ref_1، ref_2، tolerancePerFoodGr، tolerancePerKilogramGr
    tolerancePerKilogramGr → 75
    ref_1 → «پیتزا» ستون i «مصرف واقعی»
    ref_2 → «پیتزا» ستون j «انحراف»
    LET(v1,#,v2,CONVERT_GR_TO_KG(@*v1),MINUS(@,v2))
    LET(v1,#,v2,MULTIPLY(v1,@),v3,CONVERT_GR_TO_KG(v2),MINUS(@,v3))
S-r-a282b09bfd90 · «مصرف واقعی» · 10 variant · 56 bindings · params: amFoodIds، frFoodIds، fraFoodIds، ingredientId، itFoodIds، laFoodIds، p1، p2، p3، p4، paFoodIds، ref_1، ref_10، ref_11، ref_12، ref_13، ref_14، ref_15، ref_16، ref_17، ref_18، ref_2، ref_3، ref_4، ref_5، ref_6، ref_7، ref_8، ref_9، saFoodIds، sanFoodIds، sinFoodIds، stFoodIds، steakFoodIds، table_1، table_10، table_11، table_12، table_2، table_3، table_4، table_5، table_6، table_7، table_8، table_9
    ingredientId → 5
    amFoodIds → [74, 65, 76]
    itFoodIds → [63, 73, 49, 553]
    sinFoodIds → 783
    ref_1 → «پیتزا» ستون b «—»
    ref_2 → CN
    ref_3 → DN
    table_1 → Table_SalesData_SinglePizza
    ref_4 → «پیتزا» ستون b «—»
    ref_5 → CN
    ref_6 → DN
    table_2 → Table_SalesData_AmericanPizza
    ref_7 → «پیتزا» ستون b «—»
    ref_8 → CN
    ref_9 → DN
    table_3 → Table_SalesData_ItalianPizza
    table_4 → Table_Ingredients_SinglePizza
    table_5 → Table_Ingredients_AmericanPizza
    table_6 → Table_Ingredients_ItalianPizza
    LET(v1,#,v2,{#},v3,{#},v4,{#},v5,{#},v6,{#},v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v9,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v10,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v11,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v12,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v13,getTotalFoodsIngredient(v2,v1,v7,$T,Refresher),v14,getTotalFoodsIngredient(v3,v1,v8,$T,Refresher),v15,getTotalFoodsIngredient(v4,v1,v9,$T,Refresher),v16,getTotalFoodsIngredient(v5,v1,v10,$T,Refresher),v17,getTotalFoodsIngredient(v6,v1,v11,$T,Refresher),v18,getFoodValueById(#,v12)*getIngredientValue(#,v1,$T,Refresher),v19,SUM(v13,v14,v15,v16,v17,v18),CONVERT_GR_TO_KG(v19))
    LET(v1,#,v2,#,v3,#,v4,#,v5,#,v6,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v7,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v8,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v9,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v10,getTotalFoodsIngredient(v5,v1,v9,$T,Refresher),v11,getTotalFoodsIngredient(v2,v1,v6,$T,Refresher),v12,getTotalFoodsIngredient(v3,v1,v7,$T,Refresher),v13,getTotalFoodsIngredient(v4,v1,v8,$T,Refresher),v14,SUM(v11,v10,v12,v13),CONVERT_GR_TO_KG(v14))
    LET(v1,#,v2,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v3,getFoodValueById(#,v2,Refresher)*getIngredientValue(#,v1,$T,Refresher),CONVERT_GR_TO_KG(v3))
    LET(v1,#,v2,{#},v3,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v4,getTotalFoodsIngredient(v2,v1,v3,$T,Refresher),CONVERT_GR_TO_KG(v4))
    LET(v1,#,v2,{#},v3,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getTotalFoodsIngredient(v2,v1,v3,$T,Refresher))
    LET(v1,#,v2,#,v3,{#},v4,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v5,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v6,getTotalFoodsIngredient(v2,v1,v4,$T,Refresher),v7,getTotalFoodsIngredient(v3,v1,v5,$T,Refresher),SUM(v6,v7))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher),))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher),getFoodValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getFoodValueById(#,v1,Refresher))
S-r-e17b4ed8faf8 · «مقدار دریافت از انبار» · 5 variant · 60 bindings · params: p1، p2، p3، p4، ref_1، ref_2، ref_3، table_1
    ref_1 → «پیتزا» ستون b «—»
    ref_2 → CN
    ref_3 → DN
    table_1 → Table_Pizza_Request
    p1 → 5
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),v2,getIngredientValueById(#,v1,Refresher),CONVERT_GR_TO_KG(v2))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),getIngredientValueById(#,v1,Refresher))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
    LET(v1,GET_ROW_BY_PERSIAN_DATE(@,@,@,$T),SUM(getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher),getIngredientValueById(#,v1,Refresher)))
S-rec-16b45c5a1403 · «کانتر» · gozaresh_markazi__s7 (chalebagh)، gozaresh_naharkhoran__s6 (naharkhoran)
    fields: c_b=—[string]، c_e=موجودی اول شب[number]، c_f=مقدار دریافت از انبار[number]، c_g=موجودی آخر شب[number]، c_h=مصرف اعلامی[number]، c_i=مصرف واقعی[number]، c_j=انحراف[number]
    header notes: e: کانتر
    row labels: r10=تعداد آب معدنی، r6=تعداد نوشابه قوطی، r7=تعداد نوشابه خانواده، r8=تعداد دوغ، r9=تعداد دلستر
S-rec-33084d66d76a · «پیتزا» · gozaresh_markazi__s4 (chalebagh)، gozaresh_naharkhoran__s2 (naharkhoran)
    fields: c_b=—[string]، c_e=موجودی اول شب[number]، c_f=مقدار دریافت از انبار[number]، c_g=موجودی آخر شب[number]، c_h=مصرف اعلامی[number]، c_i=مصرف واقعی[number]، c_j=انحراف[number]، c_k=تعداد فروش[number]، c_l=انحراف (با تلورانس)[number]، c_m=انحراف به ازای هر عدد (با تلورانس)[number]
    header notes: e: پیتزا (تمام وزن ها به کیلوگرم است)
    row labels: r10=وزن مرغ پیتزا، r11=وزن گوشت چرخ کرده، r12=وزن کباب ترکی، r13=وزن استیک، r14=وزن فیلادلفیا، r15=وزن سوسیس کراکف، r6=وزن پنیر پیتزا، r7=وزن گوشت رست بیف، r8=وزن ژامبون سه گانه، r9=وزن پپرونی
S-rec-4559ed2575eb · «فرنگی» · gozaresh_markazi__s5 (chalebagh)، gozaresh_naharkhoran__s4 (naharkhoran)
    fields: c_b=—[string]، c_e=موجودی اول شب[number]، c_f=مقدار دریافت از انبار[number]، c_g=موجودی آخر شب[number]، c_h=مصرف اعلامی[number]، c_i=مصرف واقعی[string]، c_j=انحراف[string]، c_k=تعداد فروش[string]، c_l=انحراف (با تلورانس)[string]، c_m=انحراف به ازای هر عدد (با تلورانس)[string]
    header notes: e: فرنگی (تمام وزن ها به کیلوگرم است)
    row labels: r10=وزن گوشت رستبیف فرنگی، r11=وزن پنیر پارمیسان، r12=وزن مرغ فرنگی، r13=وزن ژامبون سیب ویژه، r14=وزن بیکن ساندویچ، r6=تعداد برگر، r7=تعداد مینی برگر، r8=تعداد هات داگ، r9=وزن گوشت چرخ کرده فرنگی
S-rec-5b04f031f49d · «سوخاری» · gozaresh_markazi__s6 (chalebagh)، gozaresh_naharkhoran__s5 (naharkhoran)
    fields: c_b=—[string]، c_e=موجودی اول شب[number]، c_f=مقدار دریافت از انبار[number]، c_g=موجودی آخر شب[number]، c_h=مصرف اعلامی[number]، c_i=مصرف واقعی[number]، c_j=انحراف[number]
    header notes: e: سوخاری
    row labels: r10=تعداد بال و کتف، r11=تعداد لقمه مرغ، r6=تعداد پرس مرغ رول سوخاری، r7=تعداد سینه مرغ، r8=تعداد فیله مرغ، r9=تعداد فیله مرغ تند
S-rec-fa0721f822cc · «تاریخ» · gozaresh_markazi__s3 (chalebagh)، gozaresh_naharkhoran__s1 (naharkhoran)
    fields: c_c=روز[number]، c_d=ماه[string]، c_e=سال[number]
    header notes: c: تاریخ
    row labels: —

## توابع فراخوانی‌شده

### GET_ROW_BY_PERSIAN_DATE (named)
```
LAMBDA(day, month, year, data, LET(\n  persianDate, FORMAT_PERSIAN_DATE(day, month, year),\n  header, INDEX(data, 1),\n  isCombinedDateFormat, IS_COMBINED_PERSIAN_DATE(INDEX(data,2, 1)),\n  \n  IF(\n    isCombinedDateFormat,\n    VSTACK(header, FILTER(data, INDEX(data,,1) = persianDate)),\n    VSTACK(header, FILTER(data, FORMAT_PERSIAN_DATE(INDEX(data, ,1), INDEX(data, ,2), INDEX(data, ,3)) = persianDate))\n  )\n))
```
### CONVERT_GR_TO_KG (named)
```
LAMBDA(weight, DIVIDE(weight,1000))
```
### getFoodValueById (script)
```
function getFoodValueById(foodId, data,refresher="") {
  return getValueById(foodId,data,'#')
}
```
### getIngredientValue (script)
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
### getIngredientValue (script)
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
### getIngredientValueById (script)
```
function getIngredientValueById(ingredientId, data,refresher="") {
  return getValueById(ingredientId,data,'##')
}
```
### getTotalFoodsCountsInRowById (script)
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
### getTotalFoodsIngredient (script)
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
### getTotalFoodsIngredient (script)
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

## زمینه

—

## جدول‌های مرتبط

S-rec-00a1c269f6e5 · «پیتزا ایتالیایی» · c_a=نام، c_b=پنیر پیتزا ##1، c_c=گوشت رست بیف ##2، c_d=ژامبون سه گانه ##3، c_e=پپرونی ##4، c_f=مرغ پیتزا ##5، c_g=گوشت چرخ کرده ##6، c_h=استیک ##8، c_i=فیلادلفیا ##9، c_j=تعداد مینی برگر ##10، c_k=سوسیس کراکف ##25، c_l=خمیر پیتزا ##26، c_m=فلفل دلمه میکس ##31، c_n=قارچ اسلایس شده ##32، c_o=سس گوجه کف ##33، c_p=سس رست بیف ##36، c_q=سس الفردو پیتزا ##37، c_r=زیتون سیاه ##30، c_s=تعداد مینی مک ##43، c_t=جعفری ##45، c_u=کارتن ایتالیایی ##54، c_v=سینگل مربع ایتالیایی ##59، c_w=سه پایه پیتزا ##63
S-rec-042805e68d8b · «موجودی اول شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=تعداد برگر ##14، c_e=تعداد مینی برگر ##10، c_f=تعداد هات داگ ##16، c_g=وزن گوشت چرخ کرده فرنگی ##23، c_h=وزن گوشت رستبیف فرنگی ##11، c_i=وزن پنیر پارمیسان ##13، c_j=وزن مرغ فرنگی ##12، c_k=ژامبون مرغ و گوشت میکس ##22، c_l=وزن بیکن ساندویچ ##15
S-rec-0f92162ffcfc · «پرسنلی» · c_a=نام، c_b=ژامبون سه گانه ##3، c_c=پنیر پیتزا ##1، c_d=خمیر پیتزا ##26
S-rec-1e279ee0f636 · «موجودی آخر شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=نوشابه قوطی مشکی ##101، c_e=نوشابه قوطی پرتقالی ##102، c_f=نوشابه قوطی اسپرایت ##104، c_g=نوشابه قوطی رژیمی ##108، c_h=دوغ سون کاله ##110، c_i=دوغ قوطی خوشگوار ##752، c_j=نوشابه خانواده مشکی ##277، c_k=نوشابه خانواده پرتقالی ##112، c_l=نوشابه خانواده سون آپ ##358، c_m=نوشابه خانواده زیرو ##374، c_n=آب معدنی ##273، c_o=دلستر استوایی ##368، c_p=دلستر لیمو ##754، c_q=لیموناد خوشگوار ##757، c_r=وزن سالاد کنتاکی ##46، c_s=تعداد مینی مک ##47، c_t=وزن جعفری ##45
S-rec-24886a08d4ab · «پاستا» · c_a=نام، c_b=مرغ فرنگی ##12، c_c=پنیر پارمیسان ##13، c_d=قارچ فرنگی ##40، c_e=پاستا پنه خام ##44، c_f=جعفری ##45
S-rec-2bd7d3188cb6 · «موجودی اول شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=نوشابه قوطی مشکی ##101، c_e=نوشابه قوطی پرتقالی ##102، c_f=نوشابه قوطی اسپرایت ##104، c_g=نوشابه قوطی رژیمی ##108، c_h=دوغ سون کاله ##110، c_i=دوغ قوطی خوشگوار ##752، c_j=نوشابه خانواده مشکی ##277، c_k=نوشابه خانواده پرتقالی ##112، c_l=نوشابه خانواده سون آپ ##358، c_m=نوشابه خانواده زیرو ##374، c_n=آب معدنی ##273، c_o=دلستر استوایی ##368، c_p=دلستر لیمو ##754، c_q=لیموناد خوشگوار ##757
S-rec-3ac3b278cadf · «استیک» · c_a=نام، c_b=مرغ فرنگی ##12، c_c=پرس دورچین استیک ##48
S-rec-58512a0deeb4 · «پیتزا امریکایی» · c_a=نام، c_b=پنیر پیتزا ##1، c_c=گوشت رست بیف ##2، c_d=ژامبون سه گانه ##3، c_e=پپرونی ##4، c_f=مرغ پیتزا ##5، c_g=گوشت چرخ کرده ##6، c_h=کباب ترکی ##7، c_i=سوسیس کراکف ##25، c_j=خمیر پیتزا ##26، c_k=فلفل دلمه میکس ##31، c_l=قارچ اسلایس شده ##32، c_m=سس گوجه کف ##33، c_n=سس کف رست بیف ##36، c_o=سس الفردو پیتزا ##37، c_p=زیتون سیاه ##30، c_q=جعفری ##45، c_r=سه پایه پیتزا ##63، c_s=کارتن امریکایی ##55
S-rec-5d323801cf94 · «موجودی آخر شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=تعداد پرس مرغ رول سوخاری ##21، c_e=تعداد سینه مرغ سوخاری ##19، c_f=تعداد فیله مرغ سوخاری ##17، c_g=تعداد فیله مرغ سوخاری تند ##18، c_h=تعداد بال و کتف ##20، c_i=تعداد لقمه مرغ سوخاری ##24، c_j=پنیر چیزا ##38، c_k=قارچ سوخاری ##39
S-rec-628ff9016caa · «موجودی آخر شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=تعداد برگر ##14، c_e=تعداد مینی برگر ##10، c_f=تعداد هات داگ ##16، c_g=وزن گوشت چرخ کرده فرنگی ##23، c_h=وزن گوشت رستبیف فرنگی ##11، c_i=وزن پنیر پارمیسان ##13، c_j=وزن مرغ فرنگی ##12، c_k=ژامبون مرغ و گوشت میکس ##22، c_l=وزن بیکن ساندویچ ##15، c_m=قارچ فرنگی ##40، c_n=نان مک ##41، c_o=نان باگت ##42، c_p=مینی مک ##43، c_q=پاستا پنه خام ##44، c_r=پرس دورچین استیک ##48
S-rec-6f06c2309913 · «ساندویچ» · c_a=نام، c_b=تعداد برگر ##14، c_c=تعداد بیکن ساندویچ ##15، c_d=تعداد هات داگ ##16، c_e=تعداد فیله مرغ سوخاری ##17، c_f=تعداد فیله مرغ سوخاری تند ##18، c_g=تعداد سینه مرغ سوخاری ##19، c_h=مرغ فرنگی ##12، c_i=گوشت رستبیف فرنگی ##11، c_j=پنیر پیتزا میکس، c_k=قارچ فرنگی ##40، c_l=تعداد نان مک ##41، c_m=تعداد نان باگت ##42، c_n=تعداد پنیر گودا پنیر گودا فرنگی ##69
S-rec-87b94d2711a8 · «سوخاری» · c_a=نام، c_b=تعداد فیله مرغ سوخاری ##17، c_c=تعداد فیله مرغ سوخاری تند ##18، c_d=تعداد سینه مرغ سوخاری ##19، c_e=تعداد بال و کتف ##20، c_f=سالاد کنتاکی##46، c_g=تعداد مینی مک کانتر ##47، c_h=قارچ سوخاری ##39، c_i=جعبه سوخاری ##53، c_j=جعبه سیب و قارچ ##52، c_k=ظرف سالاد کنتاکی ##60
S-rec-a1440cef3fb8 · «موجودی اول شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=تعداد پرس مرغ رول سوخاری ##21، c_e=تعداد سینه مرغ سوخاری ##19، c_f=تعداد فیله مرغ سوخاری ##17، c_g=تعداد فیله مرغ سوخاری تند ##18، c_h=تعداد بال و کتف ##20، c_i=تعداد لقمه مرغ سوخاری ##24، c_e=تعداد ):: که ووسینه مرغ سوخاری ##19
S-rec-bf477559ad68 · «پیتزا سینگل» · c_a=نام، c_b=پنیر پیتزا ##1، c_c=گوشت رست بیف ##2، c_d=ژامبون سه گانه ##3، c_e=پپرونی ##4، c_f=مرغ پیتزا ##5، c_g=گوشت چرخ کرده ##6، c_h=کباب ترکی ##7، c_i=سوسیس کراکف ##25، c_j=خمیر پیتزا ##26، c_k=فلفل دلمه میکس ##31، c_l=قارچ اسلایس شده ##32، c_m=سس گوجه کف ##33، c_n=سس کف رست بیف ##36، c_o=سس الفردو پیتزا ##37، c_p=زیتون سیاه ##30، c_q=جعفری ##45، c_r=کارتن امریکایی ##55، c_s=سه پایه پیتزا ##63
S-rec-bfd214478b63 · «موجودی اول شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=وزن پنیر پیتزا ##1، c_e=وزن گوشت رست بیف ##2، c_f=وزن ژامبون سه گانه ##3، c_g=وزن پپرونی ##4، c_h=وزن مرغ پیتزا ##5، c_i=وزن گوشت چرخ کرده ##6، c_j=کباب ترکی ##7، c_k=وزن استیک ##8، c_l=وزن فیلادلفیا ##9، c_m=سوسیس کراکف ##25
S-rec-d8a25df7d5be · «سالاد» · c_a=نام، c_b=مرغ فرنگی ##12، c_c=پنیر پارمیسان ##13، c_d=تعداد پرس مرغ رول سوخاری ##21، c_e=کاهو پاک شده ##27، c_f=روغن زیتون ##28، c_g=گوجه گیلاسی ##29، c_h=زیتون سیاه ##30، c_i=تعداد پنیر رول سوخاری ##38
S-rec-ddf68f27bc5d · «فرنگی» · c_a=نام، c_b=گوشت رستبیف فرنگی ##11، c_c=مرغ فرنگی ##12، c_d=پنیر پیتزا میکس، c_e=قارچ فرنگی ##40
S-rec-ecd3c0bb1713 · «لازانیا» · c_a=نام، c_b=گوشت چرخ کرده ##6، c_c=گوشت رست بیف ##2، c_d=پنیر پیتزا ##1، c_e=سس گوجه کف ##33، c_f=قارچ اسلایس شده ##32، c_g=فلفل دلمه میکس ##31، c_h=زیتون سیاه ##30
S-rec-f10f9a5c2eaa · «موجودی آخر شب» · c_a=روز، c_b=ماه، c_c=سال، c_d=وزن پنیر پیتزا ##1، c_e=وزن گوشت رست بیف ##2، c_f=وزن ژامبون سه گانه ##3، c_g=وزن پپرونی ##4، c_h=وزن مرغ پیتزا ##5، c_i=وزن گوشت چرخ کرده ##6، c_j=کباب ترکی ##7، c_k=وزن استیک ##8، c_l=وزن فیلادلفیا ##9، c_m=سوسیس کراکف ##25، c_n=سس گوجه کف پیتزا ##33، c_o=خمیر پیتزا ##26
S-rec-f344ac88fcd5 · «استارتر» · c_a=نام، c_b=پنیر پیتزا ##1، c_c=ژامبون مرغ و گوشت میکس ##22، c_d=گوشت چرخ کرده فرنگی ##23، c_e=تعداد لقمه مرغ سوخاری ##24، c_f=خمیر پیتزا ##26، c_g=قارچ سوخاری ##39، c_h=قارچ فرنگی ##40، c_i=تعداد مینی مک کانتر ##47، c_j=سالاد کنتاکی##46، c_k=جعبه سیب و قارچ ##52، c_l=جعبه سوخاری ##53، c_m=کارتن امریکایی ##55، c_n=ظرف سالاد کنتاکی ##60، c_o=سه پایه پیتزا ##63، c_p=پنیر گودا لیوانی ##74

## ورودی‌های قابل استفادهٔ مجدد

S-rec-042805e68d8b · record · موجودی اول شب
S-rec-628ff9016caa · record · موجودی آخر شب
S-rec-2bd7d3188cb6 · record · موجودی اول شب
S-rec-1e279ee0f636 · record · موجودی آخر شب
S-rec-bfd214478b63 · record · موجودی اول شب
S-rec-f10f9a5c2eaa · record · موجودی آخر شب
S-rec-1ce20a4c9a9a · record · زمان تحویل و سنجش کیفیت
S-rec-91d33a7a601c · record · ضایعات
S-rec-8a136070d6a1 · record · OFF اجرایی
S-rec-56332d3ae472 · record · نیازمندیها و مشکلات
S-rec-b831bf99eb37 · record · خمیر
S-rec-a1440cef3fb8 · record · موجودی اول شب
S-rec-5d323801cf94 · record · موجودی آخر شب
S-rec-fa0721f822cc · record · تاریخ
S-rec-33084d66d76a · record · پیتزا
S-rec-4559ed2575eb · record · فرنگی
S-rec-5b04f031f49d · record · سوخاری
S-rec-16b45c5a1403 · record · کانتر
S-rec-58512a0deeb4 · record · پیتزا امریکایی
S-rec-f344ac88fcd5 · record · استارتر
S-rec-3ac3b278cadf · record · استیک
S-rec-0f92162ffcfc · record · پرسنلی
S-rec-00a1c269f6e5 · record · پیتزا ایتالیایی
S-rec-bf477559ad68 · record · پیتزا سینگل
S-rec-ecd3c0bb1713 · record · لازانیا
S-rec-ddf68f27bc5d · record · فرنگی
S-rec-24886a08d4ab · record · پاستا
S-rec-6f06c2309913 · record · ساندویچ
S-rec-87b94d2711a8 · record · سوخاری
S-rec-d8a25df7d5be · record · سالاد
S-i-94e6d2ca8fca · item · #1 مخصوص
S-i-f18cae11689f · item · #4 رستبیف
S-i-4076e16a34cd · item · #5 قارچ سوخاری
S-i-8c956aed07ae · item · #7 اینجا باکس
S-i-d5f2bb8bb34b · item · #10 پیتزا پرسنلی
S-i-cd25866411e6 · item · #11 سیب سرخ شده
S-i-3ebcdb38a0c7 · item · #13 مکزیکانو
S-i-7d58a81c4c7f · item · #27 سیب زمینی ویژه
S-i-2a78d98590f9 · item · #44 دبل دان
S-i-c04e947323ce · item · #49 میکس
S-i-bbd832c886f9 · item · #61 اینجا پیتزا
S-i-6cdab5e7706b · item · #62 پیتزا استیک
S-i-90aad09b1ecd · item · #63 پیتزا چهارفصل
S-i-ea0abe7b0818 · item · #65 چیکن آلفردو
S-i-7947869e1f10 · item · #71 رستبیف
S-i-8ed9be7226d7 · item · #73 پیتزا چیکن باربیکیو
S-i-62444298a4a3 · item · #74 مخلوط
S-i-119fd0d403b3 · item · #75 پپرونی
S-i-5e5615aef795 · item · #76 یونانی
S-i-5c961b071f95 · item · #81 چیکن استیک
S-i-693a394a4778 · item · #82 پاستا پنه مرغ
S-i-78f02b94046d · item · #84 لازانیا رست بیف
S-i-9955cafb4eb4 · item · #85 لازانیا بلونز
S-i-3eb51bee0bf8 · item · #86 بیف استراگانف
S-i-747093514c04 · item · #87 پیتزا ناپولی
S-i-8b1aa5474fa7 · item · #120 فیله استریپس چهار تکه
S-i-9f333ccea53b · item · #122 بال و کتف سوخاری
S-i-ac127387849c · item · #123 کریسپی سینه دو تکه
S-i-008511e525a7 · item · #131 اینجا برگر
S-i-6c911b677b31 · item · #132 چیز برگر
S-i-65a1acb116a5 · item · #133 ماشروم برگر
S-i-3724b6d09329 · item · #134 دبل برگر
S-i-538c30594fd3 · item · #136 ساندویچ رستبیف
S-i-f025110444e5 · item · #137 گریل چیکن
S-i-0e60d286d3f3 · item · #138 برگر کلاسیک
S-i-dab0b4bca49a · item · #139 هات داگ
S-i-212f53b39a40 · item · #150 دبل کینگ
S-i-2433f3cc1f74 · item · #151 زینگرپلاس
S-i-69c14be191a3 · item · #303 چیکن استراگانف
S-i-ee308e663faf · item · #308 بیکن
S-i-99c17fb35da6 · item · #309 تگزاس
S-i-36af486262c3 · item · #310 پیتزا کاپری چیوسا
S-i-a0cfd6bf1228 · item · #338 سالاد کنتاکی
S-i-d9d800f547c6 · item · #348 مینی مک
S-i-0e4187476b47 · item · #350 فیله اسپایسی چهار تکه
S-i-77de2048fcfa · item · #360 نان سیر پیتزایی
S-i-ecea03854c10 · item · #385 فیله استریپس سه تکه
S-i-c7f1796d7630 · item · #386 فیله اسپایسی سه تکه
S-i-dfebc35409a7 · item · #400 دونر
S-i-6b3806b5bc0a · item · #401 سالاد سزار
S-i-595b9e7a272c · item · #402 سالاد چیزا
S-i-d2cf14b16ac7 · item · #407 سالاد چیزا با پنیر اضافه
S-i-6f38cebf9b26 · item · #504 سیب پنیر
S-i-9cebada116f5 · item · #551 سبزیجات
S-i-13d66cf4c0c0 · item · #552 فیلادلفیا
S-i-0aa517cad2c2 · item · #553 رما آلفردو
S-i-f720cead9e6a · item · #601 پاستا پستو
S-i-33f69a08e0bd · item · #766 کراکف
S-i-2722653379b8 · item · #767 مخصوص
S-i-70f2d840766e · item · #768 مخصوص
S-i-795f813bfb90 · item · #769 برگر مخصوص
S-i-e65dcba2bc15 · item · #771 مخصوص
S-i-e601667ac310 · item · #773 برگر مخصوص
S-i-18ec7cfb1d55 · item · #780 میت
S-i-705e63fe1fc0 · item · #781 پپرونی
S-i-5703f31fbd6c · item · #782 مخصوص
S-i-fbe5b87baa9f · item · #783 چیکن آلفردو
S-i-d94fead512a0 · item · #784 کراکف
S-i-a8db0529783c · item · ##1 پنیر پیتزا
S-i-42881a175bc0 · item · ##2 وزن گوشت رست بیف
S-i-e91fb84541aa · item · ##3 وزن ژامبون سه گانه
S-i-b76b08cc3b6f · item · ##4 وزن پپرونی
S-i-57211b1e6deb · item · ##5 وزن مرغ پیتزا
S-i-0c8efc5b585a · item · ##6 وزن گوشت چرخ کرده
S-i-405d34114a2d · item · ##7 کباب ترکی
S-i-e5fb10e95f6c · item · ##8 وزن استیک
S-i-9eb34b715a8e · item · ##9 وزن فیلادلفیا
S-i-cc0f76f45585 · item · ##10 تعداد مینی برگر
S-i-3792cab6320e · item · ##11 وزن گوشت رستبیف فرنگی
S-i-7241740bb61a · item · ##12 مرغ فرنگی
S-i-72c4cedee31f · item · ##13 وزن پنیر پارمیسان
S-i-543e44d531a0 · item · ##14 تعداد برگر
S-i-38ea2e6d569a · item · ##15 وزن بیکن ساندویچ
S-i-87286d352950 · item · ##16 تعداد هات داگ
S-i-8968fc14c93f · item · ##17 تعداد فیله مرغ سوخاری
S-i-0864387622a4 · item · ##18 تعداد فیله مرغ سوخاری تند
S-i-742ae51cb1a6 · item · ##19 تعداد سینه مرغ سوخاری
S-i-8e02c27fbed7 · item · ##20 تعداد بال و کتف
S-i-d57f2e2f6012 · item · ##21 تعداد پرس مرغ رول سوخاری
S-i-c28490ecc788 · item · ##22 ژامبون مرغ و گوشت میکس
S-i-9ad9a9e6080c · item · ##23 وزن گوشت چرخ کرده فرنگی
S-i-8673ff933335 · item · ##24 تعداد لقمه مرغ سوخاری
S-i-3de36fa62c0b · item · ##25 سوسیس کراکف
S-i-1db3fb0e32f9 · item · ##26 خمیر پیتزا
S-i-471b9c1b7dfb · item · ##27 کاهو پاک شده
S-i-86d7011a9ea1 · item · ##28 روغن زیتون
S-i-927a6080e6e2 · item · ##29 گوجه گیلاسی
S-i-3202462a2261 · item · ##30 زیتون سیاه
S-i-2e7714cc3e64 · item · ##31 فلفل دلمه میکس
S-i-ddd830ebd2ac · item · ##32 قارچ اسلایس شده
S-i-2f13ee8aba27 · item · ##33 سس گوجه کف
S-i-4db0b42dfe66 · item · ##36 سس کف رست بیف
S-i-aa66758f7ecc · item · ##37 سس الفردو پیتزا
S-i-e93a3bfcfaaf · item · ##38 تعداد پنیر رول سوخاری
S-i-907905be99be · item · ##39 قارچ سوخاری
S-i-dc51aaa42e2e · item · ##40 قارچ فرنگی
S-i-bbcc5df35918 · item · ##41 تعداد نان مک
S-i-4f254ac4d6a2 · item · ##42 تعداد نان باگت
S-i-063c2e2a8206 · item · ##43 تعداد مینی مک
S-i-bffaeeb73b2e · item · ##44 پاستا پنه خام
S-i-cba346d44da9 · item · ##45 جعفری
S-i-f16db2dded95 · item · ##46 سالاد کنتاکی
S-i-60a100aea128 · item · ##47 تعداد مینی مک کانتر
S-i-4de75738898d · item · ##48 پرس دورچین استیک
S-i-050adb4211ec · item · ##52 جعبه سیب و قارچ
S-i-516fb95e6a56 · item · ##53 جعبه سوخاری
S-i-0e3d38424d3d · item · ##54 کارتن ایتالیایی
S-i-5560bc5afa66 · item · ##55 کارتن امریکایی
S-i-fd08c8e4aca2 · item · ##59 سینگل مربع ایتالیایی
S-i-ed6935fdfa6c · item · ##60 ظرف سالاد کنتاکی
S-i-4b606f496e40 · item · ##63 سه پایه پیتزا
S-i-099392ba60c7 · item · ##69 تعداد پنیر گودا پنیر گودا فرنگی
S-i-a29186807c63 · item · ##74 پنیر گودا لیوانی
S-i-b783563415ef · item · ##101 نوشابه قوطی مشکی
S-i-aedf7d68705f · item · ##102 نوشابه قوطی پرتقالی
S-i-5ff5cccb2196 · item · ##104 نوشابه قوطی اسپرایت
S-i-96ca4c506199 · item · ##108 نوشابه قوطی رژیمی
S-i-508b48ca1ad3 · item · ##110 دوغ سون کاله
S-i-66b2c4f76ef8 · item · ##112 نوشابه خانواده پرتقالی
S-i-e36b25a026a2 · item · ##273 آب معدنی
S-i-a9ab76f77fc5 · item · ##277 نوشابه خانواده مشکی
S-i-4540e9a0433d · item · ##358 نوشابه خانواده سون آپ
S-i-b6372d986fd4 · item · ##368 دلستر استوایی
S-i-5d15aa766f96 · item · ##374 نوشابه خانواده زیرو
S-i-91abda2eb217 · item · ##752 دوغ قوطی خوشگوار
S-i-9b3e3fef4ffc · item · ##754 دلستر لیمو
S-i-6bf45bdc924d · item · ##757 لیموناد خوشگوار
F-00001 · record · units · واحدها

## گره‌های فرایند

cooking-024 · cooking-024-n018 · برداشت اقلام سوخاری به تعداد یا مقدار استاندارد هر آیتم طبق رسپی
cooking-026 · cooking-026-n113 · تبادل اقلام و همکاری لاین فرنگی، سالاد و گریل با لاین‌های پیتزا و سوخاری
cooking-027 · cooking-027-n025 · اعلام توقف تولید فیش کنسل‌شده به لاین‌های پیتزا، سوخاری و فرنگی
cooking-031 · cooking-031-n007 · اعلام توقف تولید فیش کنسل‌شده به لاین‌های پیتزا، سوخاری و فرنگی
cooking-022 · cooking-022-n001 · دریافت اعلام شکایت مشتری از سمت صندوق در کانتر
cooking-023 · cooking-023-n001 · سورت کردن جعبه قارچ دریافتی از انبار به قارچ کوچک و قارچ درشت در بخش سوخاری
cooking-023 · cooking-023-n005 · قرار دادن برگر روی گریل با دو تا سه دقیقه تأخیر نسبت به دریافت فیش برای هم‌زمانی با آماده شدن فیله بخش سوخاری
cooking-023 · cooking-023-n009 · پودر زدن سینه مرغ دریافتی از بخش فرنگی در لاین سوخاری
cooking-023 · cooking-023-n011 · تست کردن نان پروتان بخش فرنگی در فر لاین پیتزا
cooking-023 · cooking-023-n030 · ثبت مقدار دریافتی یا تبدیل‌شده در زیر برگه مانده آخر شب توسط بخش یا شعبه گیرنده
cooking-023 · cooking-023-n031 · ثبت مقدار تحویلی در برگه مانده آخر شب توسط بخش یا شعبه تحویل‌دهنده
cooking-024 · cooking-024-n017 · شروع تولید اقلام سوخاری طبق فیش در همان لحظه دریافت فیش
cooking-024 · cooking-024-n023 · تحویل پک آماده سوخاری به کانتر
cooking-024 · cooking-024-n028 · تحویل قارچ مازاد سورت‌شده لاین سوخاری به انبار در پایان شب
cooking-024 · cooking-024-n030 · تحویل گرفتن سینه مرغ از لاین فرنگی و آماده‌سازی آن در لاین سوخاری
cooking-024 · cooking-024-n032 · کسر خودکار مقدار انتقالی در حسابداری بر اساس تعداد سفارش‌های ثبت‌شده
cooking-025 · cooking-025-n017 · دریافت فیش سفارش پیتزا در لاین پیتزا
cooking-025 · cooking-025-n033 · تحویل جعبه پیتزا به کانتر
cooking-025 · cooking-025-n034 · دریافت سفارشات از انبار و چک کردن آنها
cooking-025 · cooking-025-n039 · تست کردن نان پروتان لاین فرنگی در فر پیتزا و تحویل آن
cooking-027 · cooking-027-n001 · جابجایی و استقرار بسته‌های بار رسیده از انبار و مرکز در کانتر
cooking-027 · cooking-027-n002 · چیدن اقلام تحویلی کانتر در یخچال و قفسه‌ها با اولویت مصرف اقلام قدیمی‌تر
cooking-027 · cooking-027-n005 · زدن جعبه‌های کارتنی پیتزا و سوخاری از حالت فلت
cooking-027 · cooking-027-n015 · تحویل گرفتن کاغذ کف پیتزا (سینگل) از انبار
cooking-027 · cooking-027-n019 · دریافت فیش کامل سفارش از پرینتر کانتر
cooking-027 · cooking-027-n030 · اعلام درخواست آیتم‌های سالن به لاین فرنگی یک تا دو دقیقه پیش از آماده شدن پیتزا
cooking-027 · cooking-027-n065 · دریافت فیش سفارش از پرینتر کانتر و گذاشتن آن روی فیش‌گیر به ترتیب نوبت
cooking-030 · cooking-030-n004 · تعیین مقدار درخواستی هر قلم برای فردا بر اساس موجودی ثبت‌شده و روز هفته
cooking-030 · cooking-030-n024 · تیک زدن و تأیید اقلام تحویلی بیش از مقدار درخواستی در برگه توسط سرپرست آشپزخانه در انبار
cooking-030 · cooking-030-n030 · اصلاح عدد برگه درخواست در انبار برای رسیدن مغایرت به حسابداری
cooking-030 · cooking-030-n044 · بررسی اشتباه کانتر در تعداد اقلام رد‌شده
cooking-031 · cooking-031-n001 · دریافت فیش کامل سفارش از پرینتر کانتر
cooking-031 · cooking-031-n019 · اعلام سیب‌ویژه سالن به لاین فرنگی پس از آماده شدن سیب سوخاری
cooking-035 · cooking-035-n004 · مراجعه لاین فرنگی به لاین پیتزا هنگام نیاز به گوشت چرخ‌کرده سیب‌ویژه
cooking-035 · cooking-035-n005 · تحویل گوشت چرخ‌کرده به لاین فرنگی از تاپینگ لاین پیتزا به اندازه پنج تا هشت گرم برای هر پرس سیب‌ویژه
cooking-035 · cooking-035-n008 · برداشتن رست‌بیف به اندازه هر پرس ساندویچ از لاین پیتزا توسط لاین فرنگی در شعبه ناهارخوران
cooking-035 · cooking-035-n010 · تحویل گرفتن مقدار روتین دورچین سبزیجات (کدو و هویج) از لاین فرنگی
cooking-035 · cooking-035-n012 · آماده کردن نان سیر در لاین پیتزا با سیر روغن گرفته‌شده از لاین فرنگی
cooking-035 · cooking-035-n014 · چاپ هم‌زمان فیش سیب‌پنیر در پرینتر لاین سوخاری و پرینتر لاین پیتزا با کد جایگاه چاپ ترکیبی پیتزا-سوخاری
cooking-035 · cooking-035-n016 · رساندن سیب سرخ‌شده از لاین سوخاری به لاین پیتزا

# Expression card

An `expr` is FEEL, and FEEL here is a closed subset. Nothing else parses.

**Keywords** — the only bare words that need no declaration:
`if` `then` `else` `and` `or` `not` `min` `max` `sum` `abs` `round` `over` `of`

**Identifiers.** Every other bare word must be declared: the `key` of one of the
rule's own `inputs[]` or `outputs[]`, or the `key` of an entry named in
`calls[]`. An identifier declared nowhere fails validation. A parameter is an
ordinary input: `{"key": "tolerance_gr", "from": {"param": "tolerancePerFoodGr"}}`
declares `tolerance_gr`, and the expression reads it by that name.

**The one aggregate form.** `sum over <input key> of ( … )` — the input key
names a record, and the identifiers inside the parentheses are that record's
field keys. There is no other loop and no other aggregate.

**`key`, never `name`.** Every member of `inputs[]`, `outputs[]`, `fields[]`,
`rows[]`, `applies_to[]`, `instances[]` is addressed by `key`.

**Minted segments** match `^[a-z][a-z0-9]*(_[a-z0-9]+)*$` — lowercase ASCII
letters, digits, single underscores. `__` joins two segments into a key and is
never typed inside one. No Persian, no capital, no dash, and never a segment
transliterated from a Persian word you guessed at.

**Never call a library function.** `GET_ROW_BY_PERSIAN_DATE`, `FILTER_BY_DATE`,
`CONVERT_GR_TO_KG` and their kind are the sheet's plumbing. State the business
computation instead.

**Worked examples**

    masraf_elami = mojudi_avval_shab + daryaft_az_anbar - mojudi_akhar_shab
    enheraf = masraf_vaqei - masraf_elami
    enheraf_ba_tolerance = enheraf - tolerance_gr / 1000 * basis
    masraf_vaqei = sum over bom of (gram_per_portion * portions_sold)


# Shape card

قرارداد بستهٔ انبار، ساخته‌شده از همان طرحواره‌ای که خروجی این واحد
در برابر آن بررسی می‌شود. کلیدی که اینجا نیامده باشد پذیرفته
نمی‌شود؛ هیچ کلیدی ساخته نمی‌شود و مقداری بیرون از فهرست مجاز هم
رد می‌شود.
`*` یعنی کلید الزامی است؛ `key` یک کلید ضرب‌شده (`a_b__c_d`) و
`segment` یک بخش از آن (`a_b`) است.

## item — data (قلم)

* category: یکی از: ingredient | product | packaging | consumable | place | other
  code: string | null
  code_absent: boolean
  grade: string | null
  group: string | null
  pack:
      size: number | null
      unit: string | null
  state: یکی از: raw | cooked | frozen | prepared | null
  tracked[]:
      reason: string | null
    * record: {"ref": "S-…"} (+ field, row)
      value: boolean | null
* unit: string | null
  unit_raw: string | null
  units[]:
      factor_to_base: یکی از این شکل‌ها —
        - number | null
        -
            max: number
            min: number
    * pack_unit: string

## record — data (جدول یا فرم)

  approved_by: string | null
  blank_master: boolean
  cadence: یکی از: nightly | shift | daily | weekly | monthly | ad_hoc | null
  day_boundary: string | null
  divergence: یکی از: none | intentional | drift | unknown | null
  fields[]:
      columns: object
      constraints:
          enum[]: any
          maximum: number
          minimum: number
          readOnly: boolean
          required: boolean
      derived: {"ref": "S-…"} یا null
      description: string | null
      filled_by: string | null
      group:
          key: segment
          title: string
    * key: segment
      refItems:
        * namespace: string
          resolved_by: یکی از: code | title
      title: string | null
      type: یکی از: string | number | integer | boolean | date
      unit: string | null
      unit_raw: string | null
  filled_by: string | null
  grain: string | null
  header_fields[]:
      columns: object
      constraints:
          enum[]: any
          maximum: number
          minimum: number
          readOnly: boolean
          required: boolean
      derived: {"ref": "S-…"} یا null
      description: string | null
      filled_by: string | null
      group:
          key: segment
          title: string
    * key: segment
      refItems:
        * namespace: string
          resolved_by: یکی از: code | title
      title: string | null
      type: یکی از: string | number | integer | boolean | date
      unit: string | null
      unit_raw: string | null
  identifier_scheme: object
  instances[]:
      branch: string یا null
      hidden: boolean
      imports[]:
        * key: key
          named_range: string | null
          range: string | null
        * source: یکی از این شکل‌ها —
            - {"ref": "S-…"} (+ field, row)
            -
              * sheet: string
              * spreadsheetId: string
    * key: key
    * sheet: string
      sheetId: integer | string | null
    * spreadsheetId: string
* location: object
* medium: یکی از: sheet | paper | external | native
  movement:
      from: {"ref": "S-…"} (+ field, row)
      reason: string | null
      to: {"ref": "S-…"} (+ field, row)
  original: string | null
  primaryKey[]: segment
  reconciled_against[]:
    * against: {"ref": "S-…"} (+ field, row)
    * cell: {field, row}
* role: یکی از: log | reference | report | config
  rows[]:
      key: key
      open: boolean
      retired: boolean
      section: segment
      supersedes: {"ref": "S-…"} یا null
      title: string | null
      unit: string | null
      unit_raw: string | null
      valid_to: 1405-05-26 یا null
      when: string | null
  sections[]:
    * key: segment
      title: string | null
  signatures[]:
    * role: string
      row_range: string | null
  stub: boolean
  template_of: {"ref": "S-…"} (+ field, row)

`location` بر حسب `medium`:
  medium=sheet: hidden، path، sheet، sheetId، spreadsheetId
  medium=paper: holder*، kept_at*
  medium=external: identifier_scheme، kept_at*، system*
  medium=native: identifier_scheme، kept_at

ستونی که خانه‌هایش نام هستند `type: string` است؛ `refItems` فقط برای خانه‌هایی است که کد `##` فهرست اقلام یا کلید یک قلم را دارند.

## measurement — data (اندازه‌گیری)

  by: string | null
  exceptions: string | null
  method: string | null
  of: {"ref": "S-…"} (+ field, row)
* quantity: یکی از: mass | count | volume | duration | money | ratio | other
* unit: string | null
  when: string | null
  writes_to: {"ref": "S-…"} (+ field, row)

## rule — data (قاعده)

  applies_to[]:
    * key: key
      params: object
      range: string | null
    * record: {"ref": "S-…"} (+ field, row)
      rows[]:
          item: string | null
        * key: key
          label: string | null
          row: integer | null
      variant: integer | string | null
  calls[]: {"ref": "S-…"} (+ field, row)
  divergence: یکی از: none | intentional | drift | unknown | null
  edge_cases[]:
      expected: any
      input: any
      why: string | null
  expr: string | null
  identifier: string | null
* inputs[]:
      from: یکی از این شکل‌ها —
        - {"ref": "S-…"} (+ field, row)
        -
          * param: string
        - یکی از: operator | calendar
        - null
    * key: segment
      title: string | null
      unit: string | null
      via: {"ref": "S-…"} (+ field, row)
  lang: یکی از: feel | table | text | sheets | gs | null
  original: string | null
* outputs[]:
    * key: segment
      nature: یکی از: standard | target | observed | limit | null
      of: {"ref": "S-…"} (+ field, row)
      per: string | null
      range:
          max: number | null
          min: number | null
      share: number | null
      title: string | null
      unit: string | null
      value: any
      writes_to: {"ref": "S-…"} (+ field, row)
  table:
      aggregate: یکی از: sum | product | min | max | null
      default: object
      hit: یکی از: first | unique | collect | null
    * inputs[]: segment
    * outputs[]: segment
    * rows[]: object
  template_of: {"ref": "S-…"} (+ field, row)
  text: string | null

`per` در خروجی یک قاعده کلید یک قلم است، نه یک نام. چهار شکل قاعده پذیرفته می‌شود: فرمول — `lang: feel` با `expr` و `inputs[]`؛ عدد ثابت — `inputs: []`، بدون `expr`، و هر خروجی با `value` یا `range`؛ سیاست بی‌فرمول — `lang: text`، `inputs[]` را نام ببر، `expr` خالی، و جملهٔ اصلی را در `original` بنویس؛ جدول تصمیم — `lang: table`، `expr` خالی، و `table` با `inputs`/`outputs` (کلیدهای همان ورودی و خروجی‌ها) و `rows[]` که هر سطر یک شیء تخت است با همان کلیدها. `nature: standard` یعنی عدد ثابت و `value` یا `range` می‌خواهد.

## note — data (یادداشت)

* about[]: {"ref": "S-…"} (+ field, row)
* question: string

## نام‌های فنی در متن نمی‌آیند

نام جدول‌ها (هر نامی که با `Table_` شروع می‌شود) و نام فایل‌ها (`.xlsx`، `.gs`) و متن فرمول‌ها در هیچ `title` یا `statement` یا `description` نمی‌آیند؛ جای آن‌ها `source[]` است.

## نمونه‌های کامل `new[]`

```json
{
  "kind": "record",
  "key": "form_tahvil_anbar",
  "title": "فرم تحویل کالا از انبار",
  "statement": "فرم کاغذی که هنگام تحویل هر قلم از انبار به لاین پر می‌شود و مقدار تحویلی و تحویل‌گیرنده را ثبت می‌کند.",
  "data": {
    "medium": "paper",
    "role": "log",
    "location": {
      "kept_at": "دفتر انبار",
      "holder": "سرپرست انبار"
    },
    "cadence": "daily",
    "grain": "هر تحویل",
    "filled_by": "انباردار",
    "approved_by": "سرپرست آشپزخانه",
    "blank_master": true,
    "fields": [
      {
        "key": "tarikh",
        "title": "تاریخ",
        "type": "date"
      },
      {
        "key": "qalam",
        "title": "نام کالا",
        "type": "string",
        "refItems": {
          "namespace": "##",
          "resolved_by": "title"
        }
      },
      {
        "key": "meqdar",
        "title": "مقدار",
        "type": "number",
        "unit": "kg"
      },
      {
        "key": "tahvil_girande",
        "title": "تحویل‌گیرنده",
        "type": "string"
      }
    ],
    "signatures": [
      {
        "role": "انباردار"
      },
      {
        "role": "سرپرست آشپزخانه"
      }
    ],
    "primaryKey": [
      "tarikh",
      "qalam"
    ]
  }
}
```

```json
{
  "kind": "measurement",
  "key": "vazn_morgh_vorudi",
  "title": "وزن مرغ ورودی",
  "statement": "وزن هر محموله مرغ هنگام تحویل با ترازوی انبار اندازه گرفته می‌شود و در فرم تحویل ثبت می‌شود.",
  "data": {
    "quantity": "mass",
    "unit": "kg",
    "method": "ترازوی دیجیتال انبار",
    "when": "هنگام تحویل محموله",
    "by": "انباردار",
    "exceptions": "محموله‌های بسته‌بندی‌شده با وزن چاپی دوباره وزن نمی‌شوند."
  }
}
```

```json
{
  "kind": "rule",
  "key": "enheraf_ba_tolerance",
  "title": "انحراف مصرف با تلورانس",
  "statement": "انحراف مصرف هر ماده اولیه پس از کسر تلورانس مجاز به دست می‌آید؛ مقدار مثبت یعنی مصرف بیش از انتظار بوده است.",
  "data": {
    "lang": "feel",
    "expr": "enheraf_ba_tolerance = enheraf - tolerance_gr / 1000 * basis",
    "inputs": [
      {
        "key": "enheraf",
        "title": "انحراف مصرف",
        "unit": "kg"
      },
      {
        "key": "tolerance_gr",
        "title": "تلورانس",
        "unit": "g",
        "from": {
          "param": "tolerancePerFoodGr"
        }
      },
      {
        "key": "basis",
        "title": "مبنای تلورانس",
        "from": {
          "param": "ref_1"
        }
      }
    ],
    "outputs": [
      {
        "key": "enheraf_ba_tolerance",
        "title": "انحراف با تلورانس",
        "unit": "kg",
        "nature": "observed"
      }
    ]
  }
}
```

```json
{
  "kind": "rule",
  "key": "mabnaye_sabt_mande",
  "title": "مبنای ثبت ماندهٔ پایان شب",
  "statement": "مبنای ثبت ماندهٔ پایان شب برای هر گروه از اقلام متفاوت است: گروهی با وزن و گروهی با تعداد ثبت می‌شوند.",
  "data": {
    "lang": "table",
    "expr": null,
    "inputs": [
      {
        "key": "goruh_qalam",
        "title": "گروه قلم"
      }
    ],
    "outputs": [
      {
        "key": "mabnaye_sabt",
        "title": "مبنای ثبت مانده"
      }
    ],
    "table": {
      "inputs": [
        "goruh_qalam"
      ],
      "outputs": [
        "mabnaye_sabt"
      ],
      "rows": [
        {
          "goruh_qalam": "بیکن ورقه‌ای",
          "mabnaye_sabt": "فقط وزن"
        },
        {
          "goruh_qalam": "نوشیدنی‌های کانتر",
          "mabnaye_sabt": "تعداد"
        }
      ]
    }
  }
}
```

## واحدهای مجاز

`unit` یکی از این نمادهاست؛ نماد دیگری تنها در صورتی پذیرفته می‌شود که همین سند آن را به صورت یک سطر تازه به رکورد واحدها (کلید `units`) اضافه کند، وگرنه رد می‌شود:
`carton`، `day`، `g`، `hour`، `irr`، `kg`، `l`، `min`، `ml`، `pack`، `pcs`، `percent`، `portion`، `ratio`، `slice`

# Style card

**`title`** — a noun phrase naming the concept. At most 60 characters, Persian,
no file, tab or cell name, no Latin except an item code.

**`statement`** — one to three sentences in the register of a written
procedure: what is measured or computed, in what unit, by whom, when; for a
record, what it is and who fills it; for an item, what it is and how it is
counted.

Never, in either field:

- an A1 address (`H6`, `$J$15`, `'پیتزا'!M6:M15`), a column letter, a tab, file
  or `Table_*` name;
- formula text, a function name, `IMPORT_FROM_SHEET`, `LET(`, `LAMBDA`,
  `.xlsx`, `.gs`;
- a schema field name, or this pipeline's vocabulary: «پاس», «اسکلت»,
  «بخش از داده‌ها», «واحد کاری», «بچ», «original», «bindings», «FEEL»,
  «account», «expr»;
- a Latin token of four letters or more — `csv`, `Excel`, `sheet`, a unit
  symbol and an item code are the only exceptions;
- a quotation, «گفته شد», «گوینده»;
- the colloquial endings «می‌زنن», «می‌کنن», «داشته باشن», «بگیم», «می‌گیم»;
- a «…» span longer than eight words.

«ستون», «تب» and «سلول» are allowed in exactly two places: a record's own
`statement`, and a field's `description`.

**Worked pair**

before — «ستون J تب پیتزا (گروه J6:J15): انحراف برابر است با مصرف واقعی منهای
مصرف اعلامی.»

after — «انحراف مصرف هر مادهٔ اولیه در پایان شب برابر است با مصرف واقعی
(برآوردشده از فروش و نسخهٔ غذاها) منهای مصرف اعلامی لاین. مقدار منفی یعنی لاین
بیش از انتظار مصرف کرده است.»

A quote belongs in `source[].quote`, a locator in `source[]`, a rival reading in
`accounts[].statement` — never in a title or a statement.
