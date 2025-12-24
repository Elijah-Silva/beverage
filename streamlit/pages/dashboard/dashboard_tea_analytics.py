import streamlit as st
import pandas  as pd
import altair as alt


csv_file_path = "/home/elijah/beverage/data/raw/"

def main():
    # Load csv files
    df_products = pd.read_csv(csv_file_path + "products.csv")
    df_order_items = pd.read_csv(csv_file_path + "order_items.csv")
    df_orders = pd.read_csv(csv_file_path + "orders.csv")
    df_sessions = pd.read_csv(csv_file_path + "sessions.csv")
    df_extractions = pd.read_csv(csv_file_path + "extractions.csv")
    df_session_batch_inventory = pd.read_csv(
        csv_file_path + "session_batch_inventory.csv"
    )
    st.title('Tea Drinking Trends')
    df_sessions = df_sessions[df_sessions['session_type'].isin(['Tea'])]
    df_sessions['session_date'] = pd.to_datetime(df_sessions['session_date'], format='ISO8601')


    st.subheader('Tea\'s per day')
    # Count coffees per day
    daily_data = df_sessions.groupby(pd.Grouper(key='session_date', freq='D')).size().reset_index(name='coffee_count')
    # Create a bar chart
    st.bar_chart(daily_data.set_index('session_date')['coffee_count'], y_label="Count")

    st.subheader('Brews by hour')
    time_data = df_sessions.copy()
    time_data['session_date'] = pd.to_datetime(time_data['session_date'])
    time_data['session_time'] = time_data['session_date'].dt.time
    time_data['hour'] = time_data['session_time'].apply(lambda t: t.hour)
    hour_counts = time_data['hour'].value_counts().reset_index()
    hour_counts.columns = ['hour', 'count']
    chart = alt.Chart(hour_counts).mark_bar().encode(
        x=alt.X('hour:O', axis=alt.Axis(labelAngle=0)),  # 0 degrees = horizontal
        y='count'
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader('Brew rating over time')
    daily_rating = df_sessions[['session_date', 'rating']]
    daily_rating = daily_rating.groupby(pd.Grouper(key='session_date', freq='D')).mean().reset_index()
    st.bar_chart(data=daily_rating, x='session_date', y='rating')

    st.subheader('Most popular drinking spots')
    st.text('In development')

if __name__ == '__main__':
    main()