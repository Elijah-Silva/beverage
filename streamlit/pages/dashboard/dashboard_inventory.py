import streamlit as st
import pandas  as pd
import psycopg2

def main():
    csv_file_path = "/home/elijah/beverage/data/raw/"
    df_products = pd.read_csv(csv_file_path + "products.csv")

    conn = psycopg2.connect(
        host="localhost",   # or mini PC IP
        dbname="beverage",
        user="elijah",
        password="2483",
        port=5432
    )

    cur = conn.cursor()

    st.title('Brewing Inventory')
    st.header('Coffee')
    query = "SELECT * FROM util.v_batch_inventory_remaining;"
    df = pd.read_sql(query, conn)
    df_coffee = df.merge(df_products, on='product_name', how='left')
    df_coffee = df_coffee[df_coffee['product_type_name'] == 'Coffee']
    df_coffee = df_coffee.iloc[:, 1:6]
    st.dataframe(df_coffee.reset_index(drop=True))

    st.header('Tea')
    df_tea = df.merge(df_products, on='product_name', how='left')
    df_tea = df_tea[df_tea['product_type_name'] == 'Tea']
    df_tea = df_tea.iloc[:, 1:6]
    st.dataframe(df_tea.reset_index(drop=True))

    st.header('Equipment')
    df_products = df_products[df_products['product_type_name'] == 'Equipment']
    df_products = df_products[['product_name', 'role']]
    st.dataframe(df_products.reset_index(drop=True))


    cur.close()
    conn.close()

if __name__ == '__main__':
    main()