import streamlit as st
import json
import pandas as pd


with open("data.json")as f:
    data=json.load(f)

st.set_page_config(page_title="Industrial Analysis", layout="wide")
st.title(" IndiaMart Industries Stats")
df = pd.DataFrame(data)
    
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("total_company_listed",value=len(df))
col2.metric("total_company_products",value=df['product'].nunique())
col3.metric("total_cities_company_situated",value=df['city'].nunique())

st.table(df)

st.divider()


    
    