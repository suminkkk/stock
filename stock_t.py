import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go

# 제목
st.title("[주식 차트 대시보드]")
st.title("KOSPI")
st.subheader("KS11")

# KS11 데이터 가져오기
df = fdr.DataReader('KS11')
df.reset_index(inplace=True) 

# 데이터프레임의 인덱스를 날짜 열로 변경
df = df.reset_index()

# 캔들스틱 차트 생성
def plot_stock_chart(symbol, start_date, end_date):
    df = fdr.DataReader(symbol, start_date, end_date)
    fig = go.Figure(data=go.Candlestick(x=df.index,
                                   open=df['Open'],
                                   high=df['High'],
                                   low=df['Low'],
                                   close=df['Close']))
    st.plotly_chart(fig)

# 차트 출력 
symbol = 'ks11'  
start_date = '2022-05-01'
end_date = '2023-05-31'


tab1, tab2, tab3 = st.tabs(['년' , '월', '일'])
with tab1:
    plot_stock_chart(symbol, start_date, end_date)
with tab2:
    plot_stock_chart('ks11','2022-05-01','2022-05-31')
with tab3:
    plot_stock_chart('ks11','2022-05-02','2022-05-03')
