import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import yfinance as yf
import datetime


class StockDashboard:
    def __init__(self):
        self.kospi_list = None
        self.symbol_idx = None
        
    # 사용자로부터 주식 종목 입력받기
    def select_symbol(self):
        # 주식 종목 리스트
        self.kospi_list = fdr.StockListing('KOSPI')
        kospi_names = self.kospi_list['Name'].tolist()

        # 주식 종목 선택 드롭다운 메뉴
        self.symbol_idx = st.selectbox("KOSPI 주식 종목 선택", kospi_names)
    
    # 사용자로부터 시작 날짜와 종료 날짜 입력 받기
    def select_dates(self):
        col1, col2 = st.columns(2)
        with col1:
            current_date = datetime.date.today()
            start_date_default = current_date.replace(day=1)
            self.start_date = st.date_input("시작 날짜", value=start_date_default)
        with col2:
            self.end_date = st.date_input("종료 날짜")

    def plot_stock_chart(self):
        # 날짜를 문자열로 변환
        start_date_str = self.start_date.strftime("%Y-%m-%d")
        end_date_str = self.end_date.strftime("%Y-%m-%d")

        # 매트릭 생성 
        code = self.kospi_list.loc[self.kospi_list['Name'] == self.symbol_idx, 'Code'].values[0]
        df = fdr.DataReader(code, start_date_str, end_date_str)
        st.metric(label=self.symbol_idx, value=df['Close'].iloc[-1], delta=f"{df['Change'].iloc[-1]:.2f}%")

        # 캔들스틱 차트 생성
        fig = go.Figure(data=go.Candlestick(x=df.index,
                                       open=df['Open'],
                                       high=df['High'],
                                       low=df['Low'],
                                       close=df['Close']))
        st.plotly_chart(fig)

    def main(self):
        # 제목
        st.title("KOSPI")

        self.select_symbol()
        self.select_dates()
        self.plot_stock_chart()


# 한국시장 선택에따른 대시보드 
class StockRankingDashboard:
    def __init__(self):
        self.market = None

    def select_market(self):
        self.market = st.selectbox("주식시장을 선택하세요", ["KRX", "KOSPI", "KOSDAQ", "KONEX"])

    # 주식 시가 총액 상위 10개 종목 데이터 가져오기
    def get_marcap_ranking(self):
        df_marcapRanking = fdr.StockListing(self.market)  # KRX 시장의 주식 목록 가져오기
        df_marcapRanking = df_marcapRanking[['Name', 'Marcap']]  # 필요한 컬럼 선택
        df_marcapRanking = df_marcapRanking.nlargest(10, 'Marcap')  # 시가 총액 상위 10개 종목 선택

        # 시가 총액 순위별로 정렬
        df_marcapRanking = df_marcapRanking.sort_values(by='Marcap', ascending=True)

        return df_marcapRanking

    # 주식 등락률 상위 10개 종목 데이터 가져오기
    def get_change_ranking(self):
        df_changeRanking = fdr.StockListing(self.market)  # KRX 시장의 주식 목록 가져오기
        df_changeRanking = df_changeRanking[['Name', 'Open','Changes', 'ChagesRatio']]  # 필요한 컬럼 선택
        df_changeRanking = df_changeRanking.nlargest(10, 'ChagesRatio')  # 등락률 상위 10개 종목 선택
        df_changeRanking['ChagesRatio'] = df_changeRanking['ChagesRatio'].apply(lambda x: f"{x:.2f}%")  # 등락률 포맷 변경

        return df_changeRanking

    # 막대 그래프 생성
    def display_marcap_chart(self, df_marcapRanking):
        fig = go.Figure(data=go.Bar(
            x=df_marcapRanking['Marcap'] / 1e12 if self.market != 'KONEX' else df_marcapRanking['Marcap'] / 1e8,
            y=df_marcapRanking['Name'],
            orientation='h',
            text=df_marcapRanking['Marcap'] / 1e12 if self.market != 'KONEX' else df_marcapRanking['Marcap'] / 1e8,
            texttemplate='%{text:.0f} 조' if self.market != 'KONEX' else '%{text:.0f}억',
            textposition='outside',
        ))

        # 레이아웃 설정
        fig.update_layout(
            title=self.market + ' 상위 10개 종목의 시가 총액',
            xaxis=dict(title='시가 총액 (조)' if self.market != 'KONEX' else '시가 총액 (억)'),
            yaxis=dict(title='종목명'),
            bargap=0.1
        )

        # 차트 출력
        st.plotly_chart(fig)

    # 등락률 테이블 출력
    def display_change_table(self, df_changeRanking):
        table_html = df_changeRanking.to_html(index=False)
        table_html_with_title = f"<h2>{self.market}급등주식 TOP10</h2>{table_html}"

        # Display HTML table using st.write
        st.write(table_html_with_title, unsafe_allow_html=True)
   

    def main(self):
       
        self.select_market()

        df_marcapRanking = self.get_marcap_ranking()
        df_changeRanking = self.get_change_ranking()
        df_changeRanking = df_changeRanking.rename(columns={'Name': '종목명', 'Open': '시가','Changes':'등락', 'ChagesRatio': '등락률'})

        self.display_marcap_chart(df_marcapRanking)
        self.display_change_table(df_changeRanking)

if __name__ == '__main__':
     # 제목
    st.title("[주식 차트 대시보드]")

    stock_dashboard = StockDashboard()
    stock_dashboard.main()

    stock_rankingDashboard = StockRankingDashboard()
    stock_rankingDashboard.main()
