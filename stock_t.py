import streamlit as st
import pandas as pd
import os


    df = pd.read_excel(os.getcwd()+'2008_2022_연령별인구현황_월간.xlsx')
    st.dataframe(df)
