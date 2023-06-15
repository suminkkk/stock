import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup

def main():
    # 제목
    st.title("[주식 차트 대시보드]")
    st.title("KOSPI")
    st.subheader("KS11")

    symbol = 'KS11'

    # 사용자로부터 시작 날짜와 종료 날짜 입력 받기
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작 날짜")
    with col2:
        end_date = st.date_input("종료 날짜")

    # 날짜를 문자열로 변환
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # 캔들스틱 차트 생성
    @st.cache_data
    def plot_stock_chart(symbol, start_date, end_date):
        df = fdr.DataReader(symbol, start_date, end_date)
        fig = go.Figure(data=go.Candlestick(x=df.index,
                                       open=df['Open'],
                                       high=df['High'],
                                       low=df['Low'],
                                       close=df['Close']))
        st.plotly_chart(fig)

    # 차트 출력
    plot_stock_chart(symbol, start_date_str, end_date_str)

    # 날짜 하드코딩
    tab1, tab2, tab3, tab4 = st.tabs(['1일' , '3개월', '1년','3년'])
    with tab1:
        plot_stock_chart(symbol,'2022-05-03','2022-05-04')
    with tab2:
        plot_stock_chart(symbol,'2022-05-01','2022-07-31')
    with tab3:
        plot_stock_chart(symbol,'2021-05-01','2022-05-31')
    with tab4:
        plot_stock_chart(symbol, '2020-05-01','2022-05-31')

def get_popular_search_keywords():
    url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSPI'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    keyword_elements = soup.select('.type_r1')
    keywords = [keyword.text for keyword in keyword_elements]
    st.text(keywords)
    
    return keywords[:5]
    



if __name__ == '__main__':
    main()
    popular_keywords = get_popular_search_keywords()
    for i, keyword in enumerate(popular_keywords, 1):
        print(f"{i}. {keyword}")
