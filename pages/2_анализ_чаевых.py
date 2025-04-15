import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title='анализ чаевых',
    page_icon='🍷', 
)

@st.cache_data
def load_data():
    tips = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')
    tips['time_order'] = pd.date_range(start='2023-01-01', end='2023-01-31', periods=len(tips)).to_series().sample(frac=1).reset_index(drop=True)
    return tips

tips = load_data()

def save_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf 

st.title('анализ чаевых')
st.markdown("---")

plt.style.use('ggplot')
plt.rcParams['figure.dpi'] = 300
sns.set_palette("pastel")

st.header("1. Связь размера счета и чаевых")
st.markdown("**Разделение по полу и привычке курения**")
fig1 = plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.scatterplot(data=tips[tips['sex'] == 'Male'], x='total_bill', y='tip', hue='smoker')
plt.title('Male')

plt.subplot(1, 2, 2)
sns.scatterplot(data=tips[tips['sex'] == 'Female'], x='total_bill', y='tip', hue='smoker')
plt.title('Female')

st.pyplot(fig1)
st.download_button(
    label="Скачать график 1",
    data=save_plot(fig1),
    file_name="scatterplot_by_sex.png",
    mime="image/png"
)

st.header("2. Связь суммы счета, чаевых и размера компании")

fig2 = plt.figure(figsize=(10, 6))
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='size', size='size', sizes=(50, 200))

st.pyplot(fig2)
st.download_button(
    label="Скачать график 2",
    data=save_plot(fig2),
    file_name="scatterplot_bill_tip_size.png",
    mime="image/png"
)
st.header("3. Чаевые по дням недели")

avg_tips = tips.groupby('day')['tip'].mean().sort_values(ascending=False)
fig3 = plt.figure(figsize=(8, 4))
plt.bar(avg_tips.index, avg_tips.values)
plt.xlabel('day')
plt.ylabel('average tips')
plt.ylim(0, avg_tips.max() * 1.2)
for i, h in enumerate(avg_tips):
    plt.text(i, h + 0.1, f"{h:.2f}", ha='center')

st.pyplot(fig3)

st.download_button(
    label="Скачать график 3",
    data=save_plot(fig3),
    file_name="average_tips_by_day.png",
    mime="image/png"
)

st.header("4. Размер счета по дням недели")

fig4 = plt.figure(figsize=(10, 6))
sns.boxplot(data=tips, x='day', y='total_bill', palette='pastel')
st.pyplot(fig4)

st.download_button(
    label="Скачать график 4",
    data=save_plot(fig4),
    file_name="total_bill_by_day.png",
    mime="image/png"
)

st.header("5. Сумма счетов по дням и времени приема пищи")
fig5 = plt.figure(figsize=(12, 6))
sns.boxplot(data=tips[tips.groupby(['day', 'time'])['time'].transform('count') > 1], x='day', y='total_bill', hue='time', palette='pastel')
st.pyplot(fig5)

st.download_button(
    label="Скачать график 5",
    data=save_plot(fig5),
    file_name="total_bill_by_day_time.png",
    mime="image/png"
)

st.header("6. Распределение чаевых по времени приема пищи")

fig6 = plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(data=tips[tips['time'] == 'Lunch'], x='tip', bins=10, kde=True)
plt.title('Lunch')

plt.subplot(1, 2, 2)
sns.histplot(data=tips[tips['time'] == 'Dinner'], x='tip', bins=10, kde=True)
plt.title('Dinner')

st.pyplot(fig6)

st.download_button(
    label="Скачать график 6",
    data=save_plot(fig6),
    file_name="tip_distribution_by_time.png",
    mime="image/png"
)



