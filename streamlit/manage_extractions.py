import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

csv_file_path = '/home/elijah/beverage/data/raw'

# Load CSVs
df_extractions = pd.read_csv(csv_file_path + '/extractions.csv') 

def main():
    st.title('Extraction data')
        
    st.data_editor(df_extractions)

if __name__ == '__main__':
    main()