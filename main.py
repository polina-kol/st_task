import streamlit as st

# настройка страницы

st.set_page_config(
    page_title='финансы и аналитика',
    page_icon='📊',
    layout='wide',
)
st.title('финансы и аналитика')
st.write("""
#### выберите раздел в боковом меню:
- ##### apple котировки: актуальные данные о котировках компании Apple 
- ##### анализ чаевых: визуализация датасета tips.csv
""")



