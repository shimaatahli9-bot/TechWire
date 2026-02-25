# مُراسِل

لوحة تحكم ذكية لتجميع وتنظيم أخبار التقنية باللغة العربية باستخدام الذكاء الاصطناعي.

## المميزات

- جمع أخبار تقنية من أكثر من 30 مصدر عالمي
- تلخيص وترجمة الأخبار تلقائياً باللغة العربية
- إنشاء مقالات إخبارية احترافية بالذكاء الاصطناعي
- واجهة عربية سهلة الاستخدام
- جدولة تلقائية لجلب الأخبار
- إدارة المصادر والإعدادات

## التثبيت

1. تأكد من وجود Python 3.8 أو أحدث:
```bash
python --version
```

2. انتقل إلى مجلد المشروع:
```bash
cd murrasil
```

3. أنشئ بيئة افتراضية (اختياري):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

4. ثبت المتطلبات:
```bash
pip install -r requirements.txt
```

5. عدّل ملف `.env` وأضف مفتاح OpenAI API:
```
OPENAI_API_KEY=your_actual_key_here
```

## التشغيل

```bash
python main.py
```

ثم افتح المتصفح على: http://127.0.0.1:8000

## الاستخدام

1. **جلب الأخبار**: اضغط على زر "جلب الأخبار" لجلب آخر الأخبار من المصادر
2. **الموافقة على خبر**: اضغط "كتابة الخبر" لإنشاء مقال كامل بالذكاء الاصطناعي
3. **رفض خبر**: اضغط "رفض" لاستبعاد الخبر
4. **الإعدادات**: اضغط على أيقونة الإعدادات لإدارة المصادر والنماذج

## المصادر المدعومة

- TechCrunch, The Verge, Wired, VentureBeat
- THE DECODER, Hugging Face Blog, OpenAI Blog
- arXiv (cs.AI, cs.LG, cs.CL, cs.CV)
- Reddit (r/MachineLearning, r/artificial)
- Hacker News, Product Hunt
- والمزيد...

## الخيارات المتاحة

- **نماذج AI**: GPT-4o-mini, GPT-4o, أو Ollama (llama3)
- **فترة التحديث**: 15 دقيقة، 30 دقيقة، أو ساعة
- **عمر الأخبار**: 24 ساعة، 48 ساعة، أو أسبوع

## هيكل المشروع

```
murrasil/
├── main.py          # نقطة الدخول
├── database.py      # قاعدة البيانات
├── fetcher.py       # جلب وتلخيص الأخبار
├── ai_writer.py     # كتابة المقالات
├── scheduler.py     # الجدولة
├── config.py        # الإعدادات
├── static/          # الملفات الثابتة
│   ├── index.html
│   └── app.js
└── requirements.txt
```

## الترخيص

MIT License
