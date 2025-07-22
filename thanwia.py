import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- واجهة التطبيق ----------
st.set_page_config(page_title="تحليل درجات الطلاب", layout="wide")

# ---------- تحميل البيانات ----------
@st.cache_data
def load_data():
    df = pd.read_excel(r"thanwia_data.xlsx")  # ← غيّر المسار حسب اسم الملف
    return df

df = load_data()

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
mean_score = df['total_degree'].mean()

import plotly.graph_objects as go

gauge_fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=mean_score,
    title={'text': "<b>متوسط الدرجات</b>", 'font': {'size': 24, 'color': 'white'}},
    delta={'reference': df['total_degree'].mean(), 'increasing': {'color': 'blue'}, 'decreasing': {'color': 'red'}},
    gauge={
        'axis': {
            'range': [0, df['total_degree'].max()],
            'tickwidth': 1,
            'tickcolor': "blue",
            'tickfont': {'color': 'white', 'size': 12}
        },
        'bar': {'color': "royalblue"},
        'bgcolor': "white",
        'steps': [
            {'range': [0, mean_score * 0.5], 'color': '#e6f2ff'},
            {'range': [mean_score * 0.5, mean_score], 'color': '#b3d9ff'},
            {'range': [mean_score, df['total_degree'].max()], 'color': '#f0f0f0'}
        ],
        'threshold': {
            'line': {'color': "blue", 'width': 4},
            'thickness': 0.75,
            'value': mean_score
        }
    }
))

gauge_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={'color': "blue", 'family': "Arial"},
    height=350
)


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
