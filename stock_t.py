import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import pandas as pd

st.title("KOSPI 주식 차트")
st.subheader("KS11")

# KS11 데이터 가져오기
df = fdr.DataReader('KS11')

# 인덱스를 날짜 형식으로 변환
df.index = pd.to_datetime(df.index)

# 캔들스틱 차트 생성
fig = go.Figure(data=go.Candlestick(x=df.index,
                                   open=df['Close'],
                                   high=df['High'],
                                   low=df['Low'],
                                   close=df['Close']))

# 차트 출력
st.plotly_chart(fig)
