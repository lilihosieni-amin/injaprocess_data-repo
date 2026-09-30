# u-att-9

نوع: attachment — 0 نامزد تصمیم

## نامزدها

—

## متن

### photo-AQADdA5rG7piKFF-.image · departments/preparation/attachments/.text/photo-AQADdA5rG7piKFF-.image.md · عکس: departments/preparation/attachments/photo-AQADdA5rG7piKFF-.jpg

Here is the precise and complete description of the document:

1. **The document's title:**
The main title is "فرم تبدیل آماده سازی" (Preparation Conversion Form), with a subtitle below it reading "سینه مرغ" (Chicken Breast).

2. **Every header field (label and value) printed at the top of the document:**
Located in a box at the top left of the document:
*   Label: "تاریخ............................" (Date), Value: Blank.
*   Label: "............................ کیلو" (Kilo), Value: Blank.

3. **Every column, naming its unit if one is printed or implied:**
Reading from right to left (as Farsi is written), the table has three overarching column groups:
*   Under the header "که به مواد خام زیر تبدیل می شود و تحویل انبار میگردد." (Which is converted into the following raw materials and delivered to the warehouse):
    *   Item category/name column.
    *   Unit column (specifying "کیلو" [Kilo] or "عدد" [Number] per row).
    *   A blank data-entry column.
*   Under the header "مابقی که در آماده سازی باقی مانده" (The remainder left in preparation):
    *   Two blank data-entry columns (for the first three items, merging into one column for subsequent items).
*   Under the header "جمع" (Total):
    *   One blank data-entry column.

4. **Every fixed row, in the order it appears on the page:**
Reading from top to bottom in the main body of the table:
*   "لقمه" (Nugget/Bite), split into two sub-rows for units: "کیلو" and "عدد".
*   "مرغ پیتزا تکه شده" (Diced Pizza Chicken), unit: "کیلو".
*   "مرغ چیزا" (Chicken Cheeza), split into two sub-rows for units: "کیلو" and "عدد".
*   "مرغ گریل" (Grilled Chicken), unit: "کیلو".
*   "کنار شنیسل" (Schnitzel Trim), unit: "کیلو".
*   A grouped section labeled "ضایعات" (Waste) containing two sub-items: "خون آبه" (Liquid/Blood water) and "پلاستیک" (Plastic), which share a merged unit cell of "کیلو".

5. **Any section headings, and any document-number or reference-number fields:**
*   Section headings consist of the three main overarching column titles: "که به مواد خام زیر تبدیل می شود و تحویل انبار میگردد.", "مابقی که در آماده سازی باقی مانده", and "جمع". "ضایعات" acts as a row section heading.
*   There are no document-number or reference-number fields on the page.

6. **Any shaded or read-only cells, and what marks them as such:**
The data-entry cells located under the "مابقی که در آماده سازی باقی مانده" and "جمع" columns for the last two row sections ("کنار شنیسل" and "ضایعات") are shaded in a solid light gray color. This visual shading marks them as read-only or not applicable for data entry.

7. **Any signature bands: their label, whether they are signed, and by whom if legible:**
There are no signature bands, labels, or boxes anywhere on the document.

8. **A verbatim transcription of all printed text on the page:**
تاریخ............................
............................ کیلو
فرم تبدیل آماده سازی
سینه مرغ
که به مواد خام زیر تبدیل می شود و تحویل انبار میگردد.
مابقی که در آماده سازی باقی مانده
جمع
لقمه
کیلو
عدد
مرغ پیتزا تکه شده
کیلو
مرغ چیزا
کیلو
عدد
مرغ گریل
کیلو
کنار شنیسل
کیلو
ضایعات
خون آبه
پلاستیک
کیلو

handwriting: no

## زمینه

—

## جدول‌های مرتبط

—

## ورودی‌های قابل استفادهٔ مجدد

S-rec-ef021443f7dc · record · ضایعات
S-rec-9f60dda7c289 · record · خمیر
S-rec-2c141582db58 · record · خروجی آماده سازی به انبار
S-rec-e3f80534814b · record · ورودی آماده سازی از انبار
S-rec-fedf9cc0dbe1 · record · OFF اجرایی
S-rec-a680471323d6 · record · نیازمندیها و مشکلات
S-rec-3d5d67801f5d · record · بازدهی
F-00001 · record · units · واحدها

## فرایندها

فرایندهای این بخش — همه را کامل بخوانید:
  runs/facts/preparation/20260930-110041/processes/preparation.md
فرایندهای بخش‌های دیگر — اگر اقلام یا ستون‌های این جدول در آن‌ها آمده، بخوانید:
  runs/facts/preparation/20260930-110041/processes/cashier.md · صندوق
  runs/facts/preparation/20260930-110041/processes/cooking.md · پخت
  runs/facts/preparation/20260930-110041/processes/dining.md · سالن
  runs/facts/preparation/20260930-110041/processes/logistics.md · لجستیک
  runs/facts/preparation/20260930-110041/processes/procurement.md · کارپردازی
  runs/facts/preparation/20260930-110041/processes/warehouse.md · انبار

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

## record — data (جدول یا فرم)

`from` کنار `data` می‌آید: `from: ["<path exactly as printed>"]` — مسیر همان فایلی که این نوشته از روی آن خوانده شده، دقیقاً همان‌طور که در سربرگ آن فایل چاپ شده (`### <name> · <path> · عکس: …`): یک مسیر، و بیش از یکی فقط وقتی که این نوشته روی چند فایل کشیده شده است. مسیری که در همین ورودی چاپ نشده باشد کنار گذاشته می‌شود. بدون آن، این نوشته به حساب همهٔ فایل‌هایی که این واحد خوانده گذاشته می‌شود.

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
      repeat: integer
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
      repeat: integer
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
* location:
      hidden: boolean
      holder: string | null
      identifier_scheme: object
      kept_at: string | null
      path: string
      sheet: string
      sheetId: integer | string | null
      spreadsheetId: string
      system: string | null
* medium: یکی از: sheet | paper | external | native | null
  movement:
      from: {"ref": "S-…"} (+ field, row)
      reason: string | null
      to: {"ref": "S-…"} (+ field, row)
  original: string | null
  primaryKey[]: segment
  reconciled_against[]:
    * against: {"ref": "S-…"} (+ field, row)
    * cell: {field, row}
* role: یکی از: log | reference | report | config | null
  rows[]:
      key: key
      open: boolean
      retired: boolean
      section: segment
      supersedes: {"ref": "S-…"} یا null
      title: string | null
      unit: string | null
      unit_raw: string | null
      valid_to: 1405-05-26
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

ستونی که خانه‌هایش نام هستند `type: string` است؛ هر ستون دیگری هم با همان چیزی که در خانه‌ها نوشته می‌شود نوع می‌گیرد. هیچ عنوان ستونی ساخته نمی‌شود: عنوان هر ستون همان چیزی است که روی فرم یا برگه چاپ شده. دسته‌ای از ستون‌های کنار هم که نام چاپ‌شدهٔ خودشان را ندارند و با دست پر می‌شوند، یک `field` است — با عنوان سربرگ چاپ‌شدهٔ بالای آن دسته، `repeat: <شمار ستون‌ها>` و واحد چاپ‌شده — نه چند ستون شماره‌گذاری‌شده. ستونی که تنها سربرگ چاپ‌شده‌اش یک واحد است (مثل «کیلو» یا «عدد») همان کلمه را به‌عنوان `title` نگه می‌دارد؛ دو ستون با سربرگ یکسان کلید متفاوت و عنوان یکسان می‌گیرند.

## measurement — data (اندازه‌گیری)

`from` کنار `data` می‌آید: `from: ["<path exactly as printed>"]` — مسیر همان فایلی که این نوشته از روی آن خوانده شده، دقیقاً همان‌طور که در سربرگ آن فایل چاپ شده (`### <name> · <path> · عکس: …`): یک مسیر، و بیش از یکی فقط وقتی که این نوشته روی چند فایل کشیده شده است. مسیری که در همین ورودی چاپ نشده باشد کنار گذاشته می‌شود. بدون آن، این نوشته به حساب همهٔ فایل‌هایی که این واحد خوانده گذاشته می‌شود.

`home` کنار `data` می‌آید: `{"ref": "<handle>", "field"?: "<column key>"}` — جدولی که این نوشته دربارهٔ آن یا روی آن است، با شناسه‌ای که همین ورودی چاپ کرده: `S-…` از «نامزدها» یا «آنچه تا کنون ثبت شده»، `F-…` از همان فهرست، یا `N-<این واحد>-<n>` برای جدولی که همین واحد در `new[]` می‌سازد (`n` از صفر). `field` فقط برای یک ستون آن جدول، با کلید چاپ‌شده. اگر هیچ جدول فهرست‌شده‌ای جا نبود، `home` را ننویس و در یک عبارت از `statement` بگو چرا. رکورد `home` ندارد. اندازه‌گیری‌ای که در واقع یک ستون از یک فرم فهرست‌شده است، یک اندازه‌گیری با `home.field` است، نه یک جدول تازه.

  by: string | null
  exceptions: string | null
  method: string | null
  of: {"ref": "S-…"} (+ field, row) یا string | null
* quantity: یکی از: mass | count | volume | duration | money | ratio | other | null
* unit: string | null
  when: string | null
  writes_to: {"ref": "S-…"} (+ field, row)

## rule — data (قاعده)

`from` کنار `data` می‌آید: `from: ["<path exactly as printed>"]` — مسیر همان فایلی که این نوشته از روی آن خوانده شده، دقیقاً همان‌طور که در سربرگ آن فایل چاپ شده (`### <name> · <path> · عکس: …`): یک مسیر، و بیش از یکی فقط وقتی که این نوشته روی چند فایل کشیده شده است. مسیری که در همین ورودی چاپ نشده باشد کنار گذاشته می‌شود. بدون آن، این نوشته به حساب همهٔ فایل‌هایی که این واحد خوانده گذاشته می‌شود.

`home` کنار `data` می‌آید: `{"ref": "<handle>", "field"?: "<column key>"}` — جدولی که این نوشته دربارهٔ آن یا روی آن است، با شناسه‌ای که همین ورودی چاپ کرده: `S-…` از «نامزدها» یا «آنچه تا کنون ثبت شده»، `F-…` از همان فهرست، یا `N-<این واحد>-<n>` برای جدولی که همین واحد در `new[]` می‌سازد (`n` از صفر). `field` فقط برای یک ستون آن جدول، با کلید چاپ‌شده. اگر هیچ جدول فهرست‌شده‌ای جا نبود، `home` را ننویس و در یک عبارت از `statement` بگو چرا. رکورد `home` ندارد. `home` یک فرمول، جدولی است که نخستین عضو `applies_to` آن نام می‌برد.

  applies_to[]:
    * key: key
      params: object
      range: string | null
    * record: {"ref": "S-…"} (+ field, row)
      rows[]:
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
      of: {"ref": "S-…"} (+ field, row) یا string | null
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

`per` در خروجی یک قاعده می‌گوید این عدد به ازای چیست و یک عبارت کوتاه است، نه یک ارجاع. چهار شکل قاعده پذیرفته می‌شود: فرمول — `lang: feel` با `expr` و `inputs[]`؛ عدد ثابت — `inputs: []`، بدون `expr`، و هر خروجی با `value` یا `range`؛ سیاست بی‌فرمول — `lang: text`، `inputs[]` را نام ببر، `expr` خالی، و جملهٔ اصلی را در `original` بنویس؛ جدول تصمیم — `lang: table`، `expr` خالی، و `table` با `inputs`/`outputs` (کلیدهای همان ورودی و خروجی‌ها) و `rows[]` که هر سطر یک شیء تخت است با همان کلیدها. `nature: standard` یعنی عدد ثابت و `value` یا `range` می‌خواهد.

## note — data (یادداشت)

`from` کنار `data` می‌آید: `from: ["<path exactly as printed>"]` — مسیر همان فایلی که این نوشته از روی آن خوانده شده، دقیقاً همان‌طور که در سربرگ آن فایل چاپ شده (`### <name> · <path> · عکس: …`): یک مسیر، و بیش از یکی فقط وقتی که این نوشته روی چند فایل کشیده شده است. مسیری که در همین ورودی چاپ نشده باشد کنار گذاشته می‌شود. بدون آن، این نوشته به حساب همهٔ فایل‌هایی که این واحد خوانده گذاشته می‌شود.

`home` کنار `data` می‌آید: `{"ref": "<handle>", "field"?: "<column key>"}` — جدولی که این نوشته دربارهٔ آن یا روی آن است، با شناسه‌ای که همین ورودی چاپ کرده: `S-…` از «نامزدها» یا «آنچه تا کنون ثبت شده»، `F-…` از همان فهرست، یا `N-<این واحد>-<n>` برای جدولی که همین واحد در `new[]` می‌سازد (`n` از صفر). `field` فقط برای یک ستون آن جدول، با کلید چاپ‌شده. اگر هیچ جدول فهرست‌شده‌ای جا نبود، `home` را ننویس و در یک عبارت از `statement` بگو چرا. رکورد `home` ندارد.

* about[]: {"ref": "S-…"} (+ field, row)
* question: string | null

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
        "type": "string"
      },
      {
        "key": "meqdar",
        "title": "مقدار",
        "type": "number",
        "unit": "kg"
      },
      {
        "key": "nimesakhte",
        "title": "نیمه ساخته برگر",
        "type": "number",
        "unit": "kg",
        "repeat": 14
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
  },
  "from": [
    "departments/<بخش>/attachments/.text/photo-….image.md"
  ]
}
```

```json
{
  "kind": "measurement",
  "key": "vazn_morgh_vorudi",
  "title": "وزن مرغ ورودی",
  "home": {
    "ref": "N-…-0",
    "field": "meqdar"
  },
  "statement": "وزن هر محموله مرغ هنگام تحویل با ترازوی انبار اندازه گرفته می‌شود و در فرم تحویل ثبت می‌شود.",
  "data": {
    "quantity": "mass",
    "unit": "kg",
    "method": "ترازوی دیجیتال انبار",
    "when": "هنگام تحویل محموله",
    "by": "انباردار",
    "exceptions": "محموله‌های بسته‌بندی‌شده با وزن چاپی دوباره وزن نمی‌شوند."
  },
  "from": [
    "departments/<بخش>/attachments/.text/photo-….image.md"
  ]
}
```

```json
{
  "kind": "rule",
  "key": "enheraf_ba_tolerance",
  "title": "انحراف مصرف با تلورانس",
  "home": {
    "ref": "S-rec-…"
  },
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
  "home": {
    "ref": "S-rec-…"
  },
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
no file, tab or cell name, no Latin except `csv`, `Excel`, `sheet` or a
unit symbol.

**`statement`** — one to three sentences in the register of a written
procedure: what is measured or computed, in what unit, by whom, when; for a
record, what it is, who fills it and how often.

Never, in either field:

- an A1 address (`H6`, `$J$15`, `'پیتزا'!M6:M15`), a column letter, a tab, file
  or `Table_*` name;
- formula text, a function name, `IMPORT_FROM_SHEET`, `LET(`, `LAMBDA`,
  `.xlsx`, `.gs`;
- a schema field name, or this pipeline's vocabulary: «اسکلت»,
  «بخش از داده‌ها», «واحد کاری», «original», «bindings», «FEEL»,
  «account», «expr»;
- a Latin token of four letters or more — `csv`, `Excel`, `sheet` and this
  run's unit symbols are the only exceptions;
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
