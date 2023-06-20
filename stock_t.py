import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup

def main():
    # 제목
    st.title("[주식 차트 대시보드]")
    st.title("KOSPI")

    # 주식 종목 리스트
    kospi_list = fdr.StockListing('KRX')
    kospi_names = kospi_list['Name'].tolist()
    kospi_Code = kospi_list['Code'].tolist()

    # 주식 종목 선택 드롭다운 메뉴
    symbol_idx = st.selectbox("KOSPI 주식 종목 선택", kospi_names)
    symbol = kospi_Code[kospi_names.index(symbol_idx)]

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

def ranking():
    # 주식 시가 총액 상위 20개 종목 데이터 가져오기
    df_ranking = fdr.StockListing('KRX')  # KRX 시장의 주식 목록 가져오기
    df_ranking = df_ranking[['Name', 'Marcap']]  # 필요한 열 선택
    df_ranking = df_ranking.nlargest(10, 'Marcap')  # 시가 총액 상위 20개 종목 선택

    # 시가 총액 순위별로 정렬
    df_ranking = df_ranking.sort_values(by='Marcap', ascending=True)

    # 막대 그래프 생성
    fig = go.Figure(data=go.Bar(
        x=df_ranking['Marcap'] / 1e12,
        y=df_ranking['Name'],
        orientation='h',
        text=df_ranking['Marcap'] / 1e12,
        texttemplate='%{text:.0f} 조',
        textposition='outside',
    ))

    # 레이아웃 설정
    fig.update_layout(
        title='KRX 상위 20개 종목의 시가 총액',
        xaxis=dict(title='시가 총액 (조)'),
        yaxis=dict(title='종목명'),
        bargap=0.1
    )

    # 차트 출력
    st.plotly_chart(fig)

    
if __name__ == '__main__':
    main()
    ranking()
