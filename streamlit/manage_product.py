import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

csv_file_path = '/home/elijah/beverage/data/raw'

# Load CSVs
df_products = pd.read_csv(csv_file_path + '/products.csv') 

def main():
    st.title('Product data')
        
    st.data_editor(df_products)

if __name__ == '__main__':
    main()