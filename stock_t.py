import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go



st.title("주식 차트 시각화 프로젝트")
st.header("KOSPI")
st.subheader("www")

def plot_stock_chart(symbol, start_date, end_date):
    df = fdr.DataReader(symbol, start_date, end_date)
    
    fig = go.Figure(data=go.Candlestick(x=df.index,
                                        open=df["Open"],
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
