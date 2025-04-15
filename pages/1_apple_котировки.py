import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# настройка страницы

st.set_page_config(
    page_title='apple котировки',
    page_icon='📈',
    layout='wide',
)

st.title('apple котировки')
st.markdown("---")

# кэширование данных

@st.cache_data
def load_data(start_date, end_date):
    return yf.download('AAPL', start=start_date, end=end_date)

# все элементы сайдбар, человек может выбирать промежуток времени 
# загрузка файла
# время - (1 вариант: вручную вбивать 2 вариант: через радио выбират предложенные промежутки(по умолчанию произвольный стоит))
# тип графика выбирается через радио свеча или линия


with st.sidebar:                       
    st.header('Настройка графика')
    choose_time_radio = st.radio(
        'Выберите промежуток времени для анализа:', 
        [
            'Произвольный',
            '1 месяц', 
            '3 месяца', 
            '6 месяцев', 
            '1 год',
            '2 года',
            '3 года'
        ], 
        index=0
    )

    DEFAULT_END = datetime.now().date()
    default_start = DEFAULT_END - pd.Timedelta(days=30)

    # вычисление дат выбранного промежутка

    if choose_time_radio != 'Произвольный':
        time ={
            '1 месяц': 30,
            '3 месяца': 90,
            '6 месяцев': 180,
            '1 год': 365,
            '2 года': 730,
            '3 года': 1095
        }
        default_start = DEFAULT_END - pd.Timedelta(days=time[choose_time_radio])

    start_date = st.date_input('Начальная дата:', default_start)
    end_date = st.date_input('Конечная дата:', DEFAULT_END)


    choose_chart = st.radio(
        'Выберите тип графика:',
        ['Линейный', 'Свечной'],
        index=0
    )


if start_date >= end_date:
    st.error('Ошибка: Начальная дата должна быть раньше конечной!')
else:
    st.write(f"Выбранные даты: {start_date} -> {end_date}")

    data = load_data(start_date, end_date)
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = data.reset_index()

    st.write(f"Загружено данных: {len(data)} записей")
    st.write(data.head(3))
    st.markdown("---")

    if choose_chart == 'Линейный':
        fig = go.Figure(data=[go.Scatter(x=data['Date'], y=data['Close'], mode='lines')])
    else:
        fig = go.Figure(data=[go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])

    fig.update_layout(
        xaxis_title='дата',
        yaxis_title='цена',
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig, use_container_width=True)




