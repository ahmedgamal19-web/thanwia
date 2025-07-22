import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# إعدادات الصفحة
st.set_page_config(page_title="نتيجة الثانوية العامة 2025", layout="centered")

# عنوان التطبيق
st.title("📊 نتيجة الثانوية العامة 2025")
st.markdown("### 🎓 ارفع ملف النتيجة (Excel) لعرض البيانات وتحليلها")

# رفع الملف
uploaded_file = st.file_uploader("🗂️ اختر ملف Excel", type=["xlsx"])

if uploaded_file is not None:
    # قراءة البيانات
    @st.cache_data
    def load_data(file):
        return pd.read_excel(file)
    
    df = load_data(uploaded_file)

    # عرض أول 5 صفوف
    st.markdown("#### 👇 معاينة أول 5 صفوف من البيانات")
    st.dataframe(df.head())

    # حساب المتوسط
    if "الدرجة الكلية" in df.columns:
        avg_score = df["الدرجة الكلية"].mean()

        st.markdown("### 🎯 متوسط الدرجات")
        st.write(f"متوسط الدرجات هو: **{avg_score:.2f}** من 410")

        # رسم مقياس Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_score,
            title={'text': "متوسط الدرجة الكلية"},
            gauge={
                'axis': {'range': [0, 410]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 150], 'color': "#ffcccc"},
                    {'range': [150, 300], 'color': "#ffe699"},
                    {'range': [300, 410], 'color': "#ccffcc"},
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ العمود 'الدرجة الكلية' غير موجود في الملف. تأكد من صحة الملف.")
else:
    st.info("⬆️ من فضلك قم برفع ملف Excel لبدء عرض النتيجة.")
