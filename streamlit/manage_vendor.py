import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

csv_file_path = '/home/elijah/beverage/data/raw'

# Load CSVs
df_vendors = pd.read_csv(csv_file_path + '/vendors.csv') 

def main():
    st.title('Vendor data')
        
    st.data_editor(df_vendors)

if __name__ == '__main__':
    main()