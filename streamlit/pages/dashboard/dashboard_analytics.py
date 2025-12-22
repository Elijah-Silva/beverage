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
    st.title('Coffee Brewing Trends')
    df_sessions = df_sessions[df_sessions['session_type'].isin(['Coffee'])]
    df_sessions['session_date'] = pd.to_datetime(df_sessions['session_date'], format='ISO8601')


    st.subheader('Espressos per day')
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

    st.subheader('Grind size over time')
    df = df_sessions.copy()
    df['session_date'] = pd.to_datetime(df['session_date'])
    df = df.dropna(subset=['grind_size'])

    # 7-session rolling mean (event-based, not calendar-based)
    df = df.sort_values('session_date')
    df['trend'] = df['grind_size'].rolling(7, min_periods=1).mean()

    st.altair_chart(
        alt.layer(
            alt.Chart(df).mark_circle(size=60, opacity=0.4).encode(
                x='session_date:T',
                y='grind_size:Q'
            ),
            alt.Chart(df).mark_line(strokeWidth=3).encode(
                x='session_date:T',
                y='trend:Q'
            )
        ),
        use_container_width=True
    )


    st.subheader('Most popular drinking spots')
    st.text('In development')

if __name__ == '__main__':
    main()