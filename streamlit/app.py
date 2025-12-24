
import os
from datetime import datetime
from pathlib import Path
import streamlit as st

path = Path("/home/elijah/beverage/data/last_run.txt")

pages = {
    "Logs": [
        st.Page('pages/log/log_coffee.py', title='Coffee'),
        st.Page('pages/log/log_tea.py', title='Tea'),
    ],
    "Overview" : [
        st.Page('pages/dashboard/dashboard_inventory.py', title='Inventory'),
    ],
    "Analytics" : [
        st.Page('pages/dashboard/dashboard_coffee_analytics.py', title='Coffee'),
        st.Page('pages/dashboard/dashboard_tea_analytics.py', title='Tea')
    ],
    "Management": [
        st.Page('pages/manage/manage_sessions.py', title='Sessions'),
        st.Page('pages/manage/manage_product.py', title='Products'),
        st.Page('pages/manage/manage_vendor.py', title='Vendors'),
        st.Page('pages/manage/manage_order.py', title='Orders'),
        st.Page('pages/manage/manage_location.py', title='Locations'),
    ],
    "SQL": [
        st.Page('pages/sql/sql_runner.py', title='Data Explorer'),
    ]
}

def main():
    pg = st.navigation(pages)

    with st.sidebar:
        try:
            ts = float(path.read_text().strip())
            st.caption(f"Last sync: {datetime.fromtimestamp(ts):%m/%d %H:%M}")
        except:
            st.caption("Sync: unknown")
        st.write('----------'   )
    # Development utilities
    with st.sidebar.expander("Dev Tools"):
            if st.button("Clear Session State"):
                st.session_state.clear()
                st.success("Session state cleared!")

            if st.checkbox("Show Session State"):
                # Only show if session_state is not empty
                if st.session_state:
                    sorted_state = dict(sorted(st.session_state.items()))
                    st.json(sorted_state)
                else:
                    st.info("Session state is empty.")

    pg.run()

if __name__ == '__main__':
    main()