import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- واجهة التطبيق ----------
st.set_page_config(page_title="تحليل درجات الطلاب", layout="wide")

# ---------- تحميل البيانات ----------
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(uploaded_file):
    return pd.read_excel(uploaded_file)

st.title("نتيجة الثانوية العامة 2025")

uploaded_file = st.file_uploader("ارفع ملف النتيجة", type=["xlsx"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.write(df.head())
else:
    st.warning("من فضلك ارفع ملف Excel لعرض النتيجة.")


# ---------- عنوان التطبيق ----------
st.title("📊 تطبيق تحليل درجات الطلاب")
st.markdown("ابحث باسم الطالب أو رقم الجلوس، وشاهد تحليلًا كاملًا للدرجات بطريقة احترافية.")

# ---------- البحث ----------
st.subheader("🔍 البحث عن طالب")
col1, col2 = st.columns(2)

with col1:
    search_name = st.text_input("🔠 ابحث بالاسم (أو جزء منه):")
with col2:
    search_code = st.text_input("🔢 ابحث برقم الجلوس:")

filtered_df = df.copy()

if search_name:
    filtered_df = filtered_df[filtered_df['arabic_name'].str.contains(search_name.strip(), case=False, na=False)]

if search_code:
    filtered_df = filtered_df[filtered_df['seating_no'].astype(str).str.contains(search_code.strip())]

if search_name or search_code:
    st.success(f"تم العثور على {len(filtered_df)} طالب matching البحث 👇")
    st.dataframe(filtered_df)
else:
    st.info("أدخل اسم أو رقم جلوس للبحث.")

# ---------- التحليل الإحصائي ----------
st.subheader("📈 التحليل الإحصائي العام للدرجات")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔢 عدد الطلاب", len(df))

with col2:
    st.metric("📉 أقل درجة", df['total_degree'].min())

with col3:
    st.metric("📈 أعلى درجة", df['total_degree'].max())

# ---------- شكل احترافي لمتوسط الدرجات ----------
import plotly.graph_objects as go

# حساب المتوسط وأقصى درجة
mean_score = df['total_degree'].mean()
max_score = df['total_degree'].max()

# رسم عداد احترافي
gauge_fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=mean_score,
    delta={'reference': max_score / 2, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
    number={'font': {'size': 36}},
    title={'text': "<b>متوسط الدرجات</b>", 'font': {'size': 24}},
    gauge={
        'axis': {'range': [0, max_score], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "royalblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 0.4 * max_score], 'color': '#FF6B6B'},     # أحمر = ضعيف
            {'range': [0.4 * max_score, 0.7 * max_score], 'color': '#FFD93D'},  # أصفر = متوسط
            {'range': [0.7 * max_score, max_score], 'color': '#6BCB77'}  # أخضر = ممتاز
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': mean_score
        }
    }
))

gauge_fig.update_layout(
    paper_bgcolor="lavender",
    font={'color': "black", 'family': "Arial"},
    height=400,
    margin=dict(t=20, b=20, l=10, r=10)
)

st.subheader("🎯 عرض احترافي لمتوسط الدرجات")
st.plotly_chart(gauge_fig, use_container_width=True)

# ---------- رسم بياني للتوزيع ----------
st.subheader("📊 توزيع الدرجات")

fig = px.histogram(
    df,
    x='total_degree',
    nbins=50,
    title='Distribution of Total Degrees',
    labels={'total_degree': 'Total Degree'},
    color_discrete_sequence=['skyblue']
)

fig.update_layout(
    xaxis_title='Total Degree',
    yaxis_title='Number of Students',
    bargap=0.05,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

# ---------- أفضل الطلاب ----------
st.subheader("🏆 أفضل 10 طلاب")

top_students = df.sort_values(by='total_degree', ascending=False).head(10)
st.table(top_students[['seating_no', 'arabic_name', 'total_degree']])

# ---------- تحميل النتائج ----------
st.subheader("📥 تحميل البيانات المفلترة")

csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button("📥 تحميل البيانات كـ CSV", csv, file_name='filtered_students.csv', mime='text/csv')
