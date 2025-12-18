import streamlit as st
import pandas as pd

csv_file_path = '/home/elijah/beverage/data/raw/'

def main():
    st.title('Order data')

    # Load CSVs
    df_orders = pd.read_csv(csv_file_path + 'orders.csv')
    df_order_items = pd.read_csv(csv_file_path + 'order_items.csv')

    # Orders editor
    st.header('Orders')
    edited_orders = st.data_editor(df_orders, num_rows="dynamic", use_container_width=True)

    st.write('---')

    # Order items editor
    st.header('Order Items')
    edited_order_items = st.data_editor(df_order_items, num_rows="dynamic", use_container_width=True)

    st.write('---')
    if st.button("Save", use_container_width=True):
        changed = False
        if not edited_orders.equals(df_orders):
            edited_orders.to_csv(csv_file_path + 'orders.csv', index=False)
            changed = True
        if not edited_order_items.equals(df_order_items):
            edited_order_items.to_csv(csv_file_path + 'order_items.csv', index=False)
            changed = True

        if changed:
            st.success("Changes saved")
        else:
            st.info("No changes were made")

if __name__ == '__main__':
    main()
