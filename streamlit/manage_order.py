import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

csv_file_path = '/home/elijah/beverage/data/raw'

# Load CSVs
df_orders = pd.read_csv(csv_file_path + '/orders.csv') 
df_order_items = pd.read_csv(csv_file_path + '/order_items.csv') 

def main():
    st.title('Order data')
        
    st.data_editor(df_orders)
    st.data_editor(df_order_items)

if __name__ == '__main__':
    main()