import streamlit as st
import json
import pandas as pd


with open("data.json")as f:
    data=json.load(f)

st.set_page_config(page_title="IndiaMart Data Analysis", layout="wide")
st.title(" IndiaMart Stats")
df = pd.DataFrame(data)
    
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Listed Companies",value=len(df))
col2.metric("Total Products",value=df['product'].nunique())
col3.metric("Number of Cities",value=df['city'].nunique())

st.table(df)

st.divider()
    
    