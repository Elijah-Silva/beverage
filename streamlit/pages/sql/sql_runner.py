import pandas as pd
import psycopg2 
import streamlit as st

sql_query = st.text_area("Enter SQL query", height=150)

if st.button("Run Query"):
    try:
        # Connect to your DB
        conn = psycopg2.connect(
            host="localhost",
            database="beverage",
            user="elijah",
            password="2483" 
        )
        df = pd.read_sql_query(sql_query, conn)
        st.dataframe(df)
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")
