import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go

st.title("KOSPI 주식 차트")
st.subheader("KS11")

# KS11 데이터 가져오기
df = fdr.DataReader('KS11')

# 캔들스틱 차트 생성
fig = go.Figure(data=go.Candlestick(x=df.index,
                                   open=df['Open'],
                                   high=df['High'],
                                   low=df['Low'],
                                   close=df['Close']))

# 차트 출력
st.plotly_chart(fig)
