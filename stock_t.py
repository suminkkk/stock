import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import datetime


class StockDashboard:
    def __init__(self):
        self.list_kospi = None
        self.idx_symbol = None
        
    # 사용자로부터 주식 종목 입력받기
    def select_symbol(self):
        # 주식 종목 리스트
        self.list_kospi = fdr.StockListing('KOSPI')
        kospi_names = self.list_kospi['Name'].tolist()

        # 주식 종목 선택 드롭다운 메뉴
        self.idx_symbol = st.multiselect("KOSPI 주식 종목 선택", kospi_names)
    
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

        filtered_symbols = self.list_kospi[self.list_kospi['Name'].isin(self.idx_symbol)]

		#멀티셀렉트 차트/매트릭 생성
        for _, row in filtered_symbols.iterrows():
            code = row['Code']
            name = row['Name']
            df_stock = fdr.DataReader(code, start_date_str, end_date_str)
            delta_percentage = df_stock['Change'].iloc[-1] * 100

            # 매트릭
            st.metric(label=name, value=df_stock['Close'].iloc[-1], delta=f"{delta_percentage:.2f}%")
            
            # 캔들
            fig = go.Figure(data=go.Candlestick(x=df_stock.index,
                                               open=df_stock['Open'],
                                               high=df_stock['High'],
                                               low=df_stock['Low'],
                                               close=df_stock['Close']))
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

    # 주식 시가총액/급등 순위
    def get_ranking(self,type):
        df_ranking = fdr.StockListing(self.market)
        if type == 'marcap':
            df_ranking = df_ranking[['Name', 'Marcap']].nlargest(10, 'Marcap')
            df_ranking = df_ranking.sort_values(by='Marcap', ascending=True)
        elif type =='change':
            df_ranking = df_ranking[['Name', 'Open','Changes', 'ChagesRatio']].nlargest(10, 'ChagesRatio')
            df_ranking['ChagesRatio'] = df_ranking['ChagesRatio'].apply(lambda x: f"{x:.2f}%")  # 등락률 포맷 변경
        return df_ranking

    # 막대 그래프 생성
    def display_marcap_chart(self,df_ranking):
        fig = go.Figure(data=go.Bar(
            x=df_ranking['Marcap'] / 1e12 if self.market != 'KONEX' else df_ranking['Marcap'] / 1e8,
            y=df_ranking['Name'],
            orientation='h',
            text=df_ranking['Marcap'] / 1e12 if self.market != 'KONEX' else df_ranking['Marcap'] / 1e8,
            texttemplate='%{text:.0f} 조' if self.market != 'KONEX' else '%{text:.0f}억',
            textposition='outside',
        ))

        # 레이아웃 설정
        fig.update_layout(
            title=self.market + '시가 총액 TOP10',
            xaxis=dict(title='시가 총액 (조)' if self.market != 'KONEX' else '시가 총액 (억)'),
            yaxis=dict(title='종목명'),
            bargap=0.1
        )

        # 차트 출력
        st.plotly_chart(fig)

    # 등락률 테이블 출력
    def display_change_table(self, df_changeRanking):
        table_html = df_changeRanking.to_html(index=False)
        table_html_with_title = f"<h5>{self.market}급등주식 TOP10</h5>{table_html}"

        # Display HTML table using st.write
        st.write(table_html_with_title, unsafe_allow_html=True)
   

    def main(self):
       
        self.select_market()

        df_marcapRanking = self.get_ranking('marcap')
        df_changeRanking = self.get_ranking('change')
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
