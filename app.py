import streamlit as st
import datetime
import math

st.set_page_config(page_title="استخراج رمزهای روحی", layout="centered")
st.title("🔮 استخراج کامل مسیر روحی - نسخه فارسی")

st.markdown("---")

# 📥 اطلاعات پایه
name = st.text_input("نام کامل", "")
mother = st.text_input("نام مادر", "")
birth_date = st.date_input("تاریخ تولد شما", min_value=datetime.date.today() - datetime.timedelta(days=365*100), max_value=datetime.date.today())

father = st.text_input("نام پدر", "")
father_dob = st.date_input("تاریخ تولد پدر", min_value=datetime.date.today() - datetime.timedelta(days=365*100), max_value=datetime.date.today())

spouse = st.text_input("نام همسر", "")
spouse_dob = st.date_input("تاریخ تولد همسر", min_value=datetime.date.today() - datetime.timedelta(days=365*100), max_value=datetime.date.today())
spouse_mother = st.text_input("نام مادر همسر", "")

birthplace = st.text_input("محل تولد", "")

# 👶 اطلاعات فرزندان
children_names = st.text_area("نام فرزندان (هر کدام در یک خط)")
children_dobs = st.text_area("تاریخ تولد فرزندان (هر کدام در یک خط - قالب YYYY-MM-DD)")

# محاسبه ابجد
abjad_dict = {'ا':1,'ب':2,'پ':2,'ت':400,'ث':500,'ج':3,'چ':3,'ح':8,'خ':600,'د':4,
              'ذ':700,'ر':200,'ز':7,'ژ':7,'س':60,'ش':300,'ص':90,'ض':800,'ط':9,
              'ظ':900,'ع':70,'غ':1000,'ف':80,'ق':100,'ک':20,'گ':20,'ل':30,
              'م':40,'ن':50,'و':6,'ه':5,'ی':10,'ء':0,'ي':10,'ى':10,'ه‍':5,'ة':5}

def abjad(word):
    return sum(abjad_dict.get(ch, 0) for ch in word)

# فاز ماه
def moon_phase(date):
    diff = date - datetime.date(2001, 1, 1)
    days = diff.days + (diff.seconds / 86400)
    lunations = 0.20439731 + (days * 0.03386319269)
    phase_index = lunations % 1 * 8
    phases = ['🌑 محاق','🌒 هلال','🌓 تربیع اول','🌔 ماه افزاینده','🌕 بدر','🌖 ماه کاهنده','🌗 تربیع دوم','🌘 هلال پایانی']
    return phases[int(phase_index)]

# آیه قرآن از مجموع ابجد
def get_quran_verse(abjad_sum):
    total_verses = 6236
    verse_number = (abjad_sum % total_verses) + 1
    return f"آیه منتخب بر اساس ابجد: شماره {verse_number} از قرآن کریم"

# اجرای برنامه
if st.button("استخراج"):
    if not name or not mother:
        st.error("نام و نام مادر الزامی است.")
    else:
        st.markdown("### 🧮 نتایج استخراج:")
        total_abjad = abjad(name) + abjad(mother)
        st.success(f"جمع ابجد: {total_abjad}")
        st.info(get_quran_verse(total_abjad))
        st.write(f"📆 فاز ماه در تولد شما: {moon_phase(birth_date)}")
        st.write(f"📍 محل تولد: {birthplace}")

        # نمایش اطلاعات پدر و همسر
        st.write("👨‍👩‍👧‍👦 اعضای خانواده:")
        st.write(f"🧔 پدر: {father} - {father_dob}")
        st.write(f"💑 همسر: {spouse} - {spouse_dob} (مادر: {spouse_mother})")

        # فرزندان
        child_names = children_names.strip().split("\n")
        child_births = children_dobs.strip().split("\n")
        if len(child_names) != len(child_births):
            st.warning("تعداد نام فرزندان با تعداد تاریخ‌ها برابر نیست. فقط موارد معتبر بررسی می‌شود.")
        for i in range(min(len(child_names), len(child_births))):
            try:
                date_obj = datetime.datetime.strptime(child_births[i], "%Y-%m-%d").date()
                st.write(f"👶 {child_names[i]} - {date_obj} | فاز ماه: {moon_phase(date_obj)}")
            except Exception:
                st.error(f"تاریخ نامعتبر برای فرزند: {child_names[i]}")