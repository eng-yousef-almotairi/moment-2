"""Moment theme: regenerate settings + order-tabs/products fields in twilight.json.  python3 scripts/moment-fields.py"""
import json, uuid
from urllib.parse import quote
P = 'twilight.json'
d = json.load(open(P))
STORE = 'https://moment-football.com'
def cat_url(slug, cid): return f'{STORE}/{quote(slug)}/c{cid}'
def k(*a): return str(uuid.uuid5(uuid.NAMESPACE_URL, 'moment/' + '/'.join(map(str, a))))
def title(id, t): return {"id": id, "type": "static", "format": "title", "variant": "h6", "value": f"<div style='background:#111417;border-radius:10px;padding:12px;margin:8px 0 12px'><h6 style='color:#fff;font-size:14px;font-weight:bold;margin:0'>{t}</h6></div>"}
def text(id, label, value='', maxlen=160):
    return {"type": "string", "icon": "sicon-format-text-alt", "label": label, "id": id, "value": value, "required": False, "format": "text", "multilanguage": False, "placeholder": None, "minLength": 0, "maxLength": maxlen}
def url(id, label, value=''):
    return {"type": "string", "icon": "sicon-link", "label": label, "id": id, "value": value, "required": False, "format": "text", "multilanguage": False, "placeholder": "https://moment-football.com/...", "minLength": 0, "maxLength": 500}
def number(id, label, value, lo=0, hi=60):
    return {"id": id, "type": "number", "format": "integer", "label": label, "icon": "sicon-hashtag", "value": value, "required": False, "minimum": lo, "maximum": hi}
def switch(id, label, value):
    return {"type": "boolean", "icon": "sicon-toggle-off", "label": label, "id": id, "format": "switch", "required": False, "value": value, "selected": value}
def color(id, label, value):
    return {"type": "string", "icon": "sicon-format-fill", "label": label, "id": id, "value": value, "format": "color", "inputType": "color", "required": False}
def image(id, label, desc=''):
    return {"type": "string", "icon": "sicon-image", "value": None, "id": id, "label": label, "format": "image", "required": False, "placeholder": None, "description": desc}
def dropdown(id, label, options, sel):
    o = [{"label": l, "value": v, "key": k(id, v)} for l, v in options]
    return {"id": id, "type": "items", "format": "dropdown-list", "label": label, "icon": "sicon-list", "selected": [x for x in o if x['value'] == sel], "options": o, "source": "Manual", "required": False, "multichoice": False}
def category(id, label, preset=None):
    f = {"id": id, "type": "items", "format": "dropdown-list", "label": label, "icon": "sicon-keyboard_arrow_down", "selected": [], "options": [], "source": "categories", "multichoice": False, "searchable": True, "required": False}
    return f
def collection(id, label, item_label, fields, value, lo=1, hi=60):
    for f in fields: f['id'] = f'{id}.{f["id"]}'
    return {"id": id, "type": "collection", "format": "collection", "required": False, "minLength": lo, "maxLength": hi, "label": label, "item_label": item_label,
            "value": [{f'{id}.{kk}': vv for kk, vv in row.items()} for row in value], "fields": fields}

SIZES = [('صغير جدًا', 'xs'), ('صغير', 'sm'), ('متوسط (التصميم ٣)', 'md'), ('كبير', 'lg'), ('كبير جدًا', 'xl')]
WEIGHTS = [('عادي', '500'), ('متوسط', '600'), ('عريض (التصميم ٣)', '700'), ('عريض جدًا', '800')]
FONT_NAMES = ['Alexandria', 'IBM Plex Sans Arabic', 'Readex Pro', 'Noto Kufi Arabic', 'Tajawal', 'Cairo', 'Almarai', 'Rubik', 'El Messiri', 'Lalezar']
FONTS = [(f, f) for f in FONT_NAMES]
NUM_FONTS = [('Barlow Condensed (التصميم ٣)', 'Barlow Condensed'), ('Oswald', 'Oswald'), ('Bebas Neue', 'Bebas Neue'), ('نفس خط العناوين', 'same')]
LAYOUT = [('شريط يتحرك أفقيًا', 'rail'), ('شبكة ثابتة', 'grid')]
VISIBLE = [('منتجان', '2'), ('منتجان ونصف (يظهر طرف الثالث)', '2.5'), ('٣ منتجات', '3')]
COLS = [('عمودان', '2'), ('٣ أعمدة', '3'), ('٤ أعمدة', '4')]

def list_fields(p, label, layout='rail', auto=True):
    return [dropdown(f'{p}layout', f'{label}طريقة العرض', LAYOUT, layout),
            dropdown(f'{p}visible', f'{label}المنتجات الظاهرة على الجوال (للشريط)', VISIBLE, '2.5'),
            dropdown(f'{p}cols', f'{label}عدد الأعمدة على الجوال (للشبكة)', COLS, '2'),
            switch(f'{p}auto', f'{label}حركة تلقائية للشريط', auto),
            number(f'{p}speed', f'{label}سرعة الحركة: منتج كل كم ثانية', 3, 2, 15)]

# ---------- global settings ----------
new_settings = [
    title('m-ttl-colors2', 'مومنت: ألوان إضافية'),
    color('m_section_bg', 'خلفية الأقسام', '#ffffff'),
    color('m_soft', 'خلفية الصناديق الرمادية', '#f6f6f6'),
    color('m_title_color', 'لون العناوين', '#111417'),
    color('m_muted', 'لون النصوص الثانوية', '#55585b'),
    color('m_price_color', 'لون السعر', '#111417'),
    color('m_sale_color', 'لون السعر بعد الخصم', '#111417'),
    color('m_btn_bg', 'خلفية الأزرار الممتلئة', '#111417'),
    color('m_btn_fg', 'نص الأزرار الممتلئة', '#ffffff'),
    color('m_tab_active', 'خلفية التبويب النشط', '#ffffff'),
    color('m_add_bg', 'خلفية زر + على المنتج', '#ffffff'),
    color('m_add_fg', 'لون علامة +', '#111417'),
    title('m-ttl-type2', 'مومنت: أحجام الخطوط'),
    dropdown('m_title_weight', 'سماكة العناوين', WEIGHTS, '700'),
    dropdown('m_title_size', 'حجم العناوين', SIZES, 'md'),
    dropdown('m_text_size', 'حجم النصوص', SIZES, 'md'),
    dropdown('m_num_font', 'خط الأسعار والأرقام', NUM_FONTS, 'Barlow Condensed'),
    dropdown('m_price_size', 'حجم الأسعار والأرقام', SIZES, 'md'),
    switch('m_latin_digits', 'الأسعار بأرقام إنجليزية (150 بدل ١٥٠) كما في التصميم ٣', True),
    switch('m_card_qty', 'إظهار الكمية المتبقية على بطاقة المنتج', False),
    switch('m_footer_dark', 'تذييل داكن', False),
    title('m-ttl-more', 'مومنت: زر «عرض الكل»'),
    dropdown('m_more_style', 'شكل الزر', [('كبسولة ملوّنة (مقترح)', 'pill'), ('صندوق بزوايا ناعمة', 'box'), ('إطار فقط', 'outline'), ('بطاقة بزوايا مائلة', 'tag'), ('نص فقط', 'link')], 'pill'),
    color('m_more_bg', 'لون الزر', '#111417'),
    color('m_more_fg', 'لون نص الزر', '#ffffff'),
]
ids = {s['id'] for s in new_settings}
d['settings'] = [s for s in d['settings'] if s.get('id') not in ids]
# extend font lists
for s in d['settings']:
    if s.get('id') in ('m_display_font', 'm_body_font'):
        cur = s['selected'][0]['value'] if s.get('selected') else 'Alexandria'
        s.update(dropdown(s['id'], s['label'], FONTS, cur))
# insert after m_body_font
i = max(n for n, s in enumerate(d['settings']) if s.get('id') == 'm_body_font') + 1
d['settings'][i:i] = new_settings

# ---------- promo card fields (shared by «بطاقات علوية» and the hero strip in order tabs) ----------
BG_STYLES = [('لون واحد', 'solid'), ('تدرج لوني', 'gradient')]
BG_DIRS = [('قطري ↘', '135deg'), ('قطري ↙', '225deg'), ('أفقي ←', '270deg'), ('أفقي →', '90deg'), ('عمودي ↓', '180deg'), ('عمودي ↑', '0deg'), ('دائري', 'radial')]
def promo_item_fields():
    return [image('image', 'الصورة (اتركها فارغة لبطاقة ملوّنة)', 'المقاس المناسب 1200×750 بكسل'),
            text('title', 'العنوان', '', 60), text('subtitle', 'النص الفرعي', '', 100), url('url', 'الرابط'),
            dropdown('bg_style', 'خلفية البطاقة الملوّنة', BG_STYLES, 'solid'),
            color('bg_color', 'اللون الأول', '#111417'), color('bg_color2', 'اللون الثاني (للتدرج)', '#3a3f45'),
            dropdown('bg_dir', 'اتجاه التدرج', BG_DIRS, '135deg'),
            color('text_color', 'لون النص', '#ffffff'),
            switch('dark', 'إظهار ظهر القميص على البطاقة الملوّنة', True),
            text('kit_name', 'الاسم على القميص', 'MOMENT', 14), text('kit_number', 'الرقم على القميص', '10', 2),
            color('kit_color', 'لون القميص', '#c8102e')]
PROMO_DEFAULT = [
    {"title": "أرسنال 2026/27", "subtitle": "الأساسي والاحتياطي والثالث", "bg_style": "gradient", "bg_color": "#111417", "bg_color2": "#7a0c1c", "bg_dir": "135deg", "text_color": "#ffffff", "dark": True, "kit_name": "MOMENT", "kit_number": "10", "kit_color": "#d0021b", "url": cat_url('موسم-2026-2027', 2065938265)},
    {"title": "طقمك باسمك", "subtitle": "من الطلبات المخصصة", "bg_style": "gradient", "bg_color": "#111417", "bg_color2": "#3a3f45", "bg_dir": "135deg", "text_color": "#ffffff", "dark": True, "kit_name": "SALAH", "kit_number": "11", "kit_color": "#c8102e"},
    {"title": "تيشرتات كلاسيكية", "subtitle": "جاهزة للشحن", "bg_style": "gradient", "bg_color": "#0b2a5b", "bg_color2": "#111417", "bg_dir": "135deg", "text_color": "#ffffff", "dark": True, "kit_name": "CLASSIC", "kit_number": "7", "kit_color": "#0b4ea2", "url": cat_url('تيشرتات-كلاسيكة', 234133083)},
]
def fix_dropdown_values(rows):
    # collection defaults store plain values; manual dropdowns inside collections expect [{label,value}]
    return rows

# ---------- order tabs ----------
ROWS = {1: ('منتجات موسم 2026/27', cat_url('موسم-2026-2027', 2065938265), True),
        2: ('تيشرتات كلاسيكية', cat_url('تيشرتات-كلاسيكة', 234133083), True),
        3: ('', '', False)}
CLUBS = [("أرسنال", "#d0021b"), ("ليفربول", "#c8102e"), ("برشلونة", "#a50044"), ("مانشستر سيتي", "#6cabdd"),
         ("مانشستر يونايتد", "#da291c"), ("ميلان", "#111111"), ("يوفنتوس", "#f4f4f4"), ("إنتر ميلان", "#0b4ea2"),
         ("ريال مدريد", "#febe10"), ("بايرن ميونخ", "#dc052d"), ("الهلال", "#1e3f96"), ("النصر", "#f4c90e")]
f = [title('mt-hero', 'بطاقات علوية فوق التبويبات'),
     switch('hero_on', 'إظهار بطاقات علوية ملاصقة للتبويبات', True),
     dropdown('hero_ratio', 'مقاس البطاقة', [('عريضة 16:9 (التصميم ٣)', '16 / 9'), ('16:10', '16 / 10'), ('شريط 2:1', '2 / 1'), ('شريط رفيع 3:1', '3 / 1'), ('مربعة', '1 / 1')], '16 / 9'),
     switch('hero_auto', 'حركة تلقائية للبطاقات', True),
     number('hero_speed', 'تنتقل البطاقة كل كم ثانية', 4, 2, 15),
     collection('hero', 'البطاقات', 'بطاقة', promo_item_fields(), [dict(r) for r in PROMO_DEFAULT], 0, 8),
     title('mt-general', 'عام'),
     text('ready_eta', 'مدة الجاهز والأكواب (اتركه فارغًا لاستخدام إعداد الثيم)', '', 30),
     text('custom_eta', 'مدة الطلبات المخصصة (اتركه فارغًا لاستخدام إعداد الثيم)', '', 30),
     switch('sticky', 'تثبيت التبويبات أعلى الشاشة عند التمرير', True),
     title('mt-t1', 'التبويب الأول: جاهز للشحن'),
     text('t1_label', 'اسم التبويب', 'جاهز للشحن', 30),
     text('t1_note', 'الملاحظة', 'هذه المنتجات في مخزوننا، ويصلك طلبك خلال ١ إلى ٥ أيام.')]
for r, (t, link, on) in ROWS.items():
    L = f'الصف {r} · '
    f += [title(f'mt-r{r}', f'جاهز للشحن · الصف {r}'),
          switch(f'r{r}_on', f'{L}إظهار الصف', on),
          text(f'r{r}_title', f'{L}العنوان', t, 60),
          category(f'r{r}_category', f'{L}التصنيف'),
          number(f'r{r}_limit', f'{L}عدد المنتجات', 10, 1, 40),
          text(f'r{r}_more', f'{L}نص زر عرض الكل', 'عرض الكل', 30),
          url(f'r{r}_url', f'{L}رابط زر عرض الكل (فارغ = رابط التصنيف)', link),
          *list_fields(f'r{r}_', L)]
f += [title('mt-t2', 'التبويب الثاني: طلبات مخصصة'),
      text('t2_label', 'اسم التبويب', 'طلبات مخصصة', 30),
      text('t2_note', 'الملاحظة', 'يُجهّز كل طلب خصيصًا لك، ويصلك خلال ١٣ إلى ١٨ يومًا.'),
      text('t2_heading', 'العنوان', 'اختر ناديك', 60),
      collection('clubs', 'الأندية', 'نادٍ', [text('name', 'اسم النادي', '', 40), image('logo', 'الشعار', 'PNG بخلفية شفافة 300×300'),
                                             url('url', 'رابط صفحة النادي'), color('color', 'لون بديل إذا لم يُرفع شعار', '#111417')],
                 [{"name": n, "color": c} for n, c in CLUBS]),
      dropdown('logo_cols', 'عدد الأعمدة على الجوال', [('٣', '3'), ('٤', '4'), ('٥', '5')], '3'),
      dropdown('logo_shape', 'شكل الشعارات', [('بطاقة فاخرة (مقترح)', 'tile'), ('الشعار فقط بدون إطار', 'bare'), ('دائري', 'circle')], 'tile'),
      switch('logo_names', 'إظهار اسم النادي تحت الشعار', True),
      text('t2_button', 'نص الزر السفلي', 'عرض كل الطلبات المخصصة', 40),
      url('t2_url', 'رابط الزر السفلي (فارغ = بدون زر)'),
      title('mt-t3', 'التبويب الثالث: الأكواب'),
      switch('t3_enabled', 'إظهار التبويب', True),
      text('t3_label', 'اسم التبويب', 'الأكواب', 30),
      text('t3_note', 'الملاحظة', 'الأكواب في مخزوننا، ويصلك طلبك خلال ١ إلى ٥ أيام.'),
      category('t3_category', 'التصنيف'),
      number('t3_limit', 'عدد المنتجات', 24, 1, 60),
      *list_fields('t3_', '', layout='grid', auto=False),
      text('t3_more', 'نص زر عرض الكل', 'عرض كل الأكواب', 40),
      url('t3_more_url', 'رابط زر عرض الكل (فارغ = رابط التصنيف)')]
for c in d['components']:
    if c['path'] == 'home.moment-order-tabs':
        c['fields'] = f
    if c['path'] == 'home.moment-promos':
        c['fields'] = [collection('items', 'البطاقات', 'بطاقة', promo_item_fields(), [dict(r) for r in PROMO_DEFAULT], 1, 8),
                       dropdown('ratio', 'مقاس البطاقة', [('عريضة 16:9 (التصميم ٣)', '16 / 9'), ('16:10', '16 / 10'), ('شريط 2:1', '2 / 1'), ('شريط رفيع 3:1', '3 / 1'), ('مربعة', '1 / 1')], '16 / 9'),
                       switch('auto', 'حركة تلقائية للبطاقات', True),
                       number('speed', 'تنتقل البطاقة كل كم ثانية', 4, 2, 15)]
    if c['path'] == 'home.moment-products':
        keep = [x for x in c['fields'] if x.get('id') not in ('layout', 'visible', 'cols', 'auto', 'speed')]
        i = next(n for n, x in enumerate(keep) if x.get('id') == 'limit') + 1
        keep[i:i] = list_fields('', '', layout='grid', auto=True)
        c['fields'] = keep

def more_fields():
    return [title('mt-more', 'زر «عرض الكل» في هذا القسم'),
            dropdown('more_style', 'شكل الزر', [('حسب إعداد الثيم', 'theme'), ('كبسولة ملوّنة', 'pill'), ('صندوق بزوايا ناعمة', 'box'), ('إطار فقط', 'outline'), ('بطاقة بزوايا مائلة', 'tag'), ('نص فقط', 'link')], 'theme'),
            switch('more_colors_on', 'ألوان خاصة لهذا القسم', False),
            color('more_bg', 'لون الزر', '#111417'),
            color('more_fg', 'لون نص الزر', '#ffffff')]
MORE_IDS = {'mt-more', 'more_style', 'more_colors_on', 'more_bg', 'more_fg'}
for c in d['components']:
    if c['path'] in ('home.moment-order-tabs', 'home.moment-products'):
        c['fields'] = [x for x in c['fields'] if x.get('id') not in MORE_IDS] + more_fields()

# ---------- per-section text styling (every Moment section) ----------
def text_style_fields():
    t_sizes = [('حسب الثيم', 'theme')] + [(f'{n} بكسل', str(n)) for n in (16, 18, 20, 22, 24, 28, 32, 36, 40)]
    b_sizes = [('حسب الثيم', 'theme')] + [(f'{n} بكسل', str(n)) for n in (11, 12, 13, 14, 15, 16, 17, 18, 20)]
    weights = [('حسب الثيم', 'theme'), ('خفيف', '400'), ('عادي', '500'), ('متوسط', '600'), ('عريض', '700'), ('عريض جدًا', '800')]
    fonts = [('حسب خط الثيم', 'theme')] + FONTS
    out = [title('ms-ttl', 'تنسيق النصوص في هذا القسم')]
    for g, L, sizes, col in (('title', 'العناوين', t_sizes, '#111417'), ('text', 'النصوص', b_sizes, '#55585b')):
        out += [dropdown(f'{g}_font', f'خط {L}', fonts, 'theme'),
                dropdown(f'{g}_size', f'حجم {L}', sizes, 'theme'),
                dropdown(f'{g}_weight', f'سماكة {L}', weights, 'theme'),
                switch(f'{g}_color_on', f'لون مخصص لـ{L}', False),
                color(f'{g}_color', f'لون {L}', col)]
    return out
TS_IDS = {'ms-ttl'} | {f'{g}_{x}' for g in ('title', 'text') for x in ('font', 'size', 'weight', 'color_on', 'color')}
for c in d['components']:
    if c['path'].startswith('home.moment-') and c['path'] != 'home.moment-spacer':
        c['fields'] = [x for x in c['fields'] if x.get('id') not in TS_IDS] + text_style_fields()
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=4)
print('ok', len(d['settings']))
