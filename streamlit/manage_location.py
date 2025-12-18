import streamlit as st
import pandas as pd

csv_file_path = '/home/elijah/beverage/data/raw/'

def main():
    st.title('Location data')

    # Load CSV
    df_locations = pd.read_csv(csv_file_path + 'locations.csv')
    df_locations = df_locations

    # Show editor
    edited_locations = st.data_editor(df_locations, num_rows="dynamic", use_container_width=True)

    st.write('---')
    if st.button("Save", use_container_width=True):
        if not edited_locations.equals(df_locations):
            edited_locations.to_csv(csv_file_path + 'locations.csv', index=False)
            st.success("Changes saved")
        else:
            st.info("No changes were made")

if __name__ == '__main__':
    main()
