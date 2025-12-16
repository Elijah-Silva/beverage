import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

csv_file_path = '/home/elijah/beverage/data/raw'

# Load CSVs
df_locations = pd.read_csv(csv_file_path + '/locations.csv') 

def main():
    st.title('Location data')
        
    st.data_editor(df_locations)

if __name__ == '__main__':
    main()