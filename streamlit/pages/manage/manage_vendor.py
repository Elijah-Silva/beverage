import streamlit as st
import pandas as pd

csv_file_path = '/home/elijah/beverage/data/raw/'

def main():
    st.title('Vendor data')

    # Load CSV
    df_vendors = pd.read_csv(csv_file_path + 'vendors.csv')

    # Show editor
    edited_vendors = st.data_editor(df_vendors, num_rows="dynamic", use_container_width=True)
    st.write('---')
    if st.button("Save",use_container_width=True):
        if not edited_vendors.equals(df_vendors):
            edited_vendors.to_csv(csv_file_path + 'vendors.csv', index=False)
            st.success("Changes saved")
        else:
            st.info("No changes were made")

if __name__ == '__main__':
    main()
