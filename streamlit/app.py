import streamlit as st
import uuid

pages = {
    "Log": [
        st.Page('log_coffee.py', title='Coffee'),
        st.Page('log_tea.py', title='Tea'),
    ],
    "Dashboards" : [
        st.Page('dashboard_inventory.py', title='Inventory'),
        st.Page('dashboard_analytics.py', title='Analytics')
    ],
    "Manage": [
        st.Page('manage_sessions.py', title='Sessions'),
        st.Page('manage_product.py', title='Products'),
        st.Page('manage_vendor.py', title='Vendors'),
        st.Page('manage_order.py', title='Orders'),
        st.Page('manage_location.py', title='Locations'),
    ]
}

def main():
    pg = st.navigation(pages)

    # Development utilities
    with st.sidebar.expander("Development Utilities"):
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