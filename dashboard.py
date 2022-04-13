import streamlit as st
import pandas as pd
# import numpy as np
import matplotlib.pylab as plt

st.title('BigMac Index')


@st.cache
def load_data():
    data = pd.read_csv("./dataset/big-mac-source-data.csv")
    data.drop(['GDP_dollar', 'iso_a3'], axis=1, inplace=True)
    data.set_index('date')
    return data.assign(date=lambda d: pd.to_datetime(d['date']))


df = load_data()
print("aqui")
countries = st.sidebar.multiselect(
    "Select Countries",
    df['name'].unique()
)
print("oi")
varname = st.sidebar.selectbox(
    "Select Column",
    ("local_price", "dollar_price")
)

subset_df = df.loc[lambda d: d['name'].isin(countries)]

fig, ax = plt.subplots()
for name in countries:
    plotset = subset_df.loc[lambda d: d['name'] == name]
    plt.plot(plotset['date'], plotset[varname], label=name)
# plt.legend()
st.pyplot(fig)

if st.sidebar.checkbox("Show Raw Data"):
    st.markdown("### Raw Data")
    st.write(subset_df)
