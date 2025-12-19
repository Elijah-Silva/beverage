import streamlit as st

pages = {
    "Log": [
        st.Page('pages/log/log_coffee.py', title='Coffee'),
        st.Page('pages/log/log_tea.py', title='Tea'),
    ],
    "Dashboards" : [
        st.Page('pages/dashboard/dashboard_inventory.py', title='Inventory'),
        st.Page('pages/dashboard/dashboard_analytics.py', title='Analytics')
    ],
    "Manage": [
        st.Page('pages/manage/manage_sessions.py', title='Sessions'),
        st.Page('pages/manage/manage_product.py', title='Products'),
        st.Page('pages/manage/manage_vendor.py', title='Vendors'),
        st.Page('pages/manage/manage_order.py', title='Orders'),
        st.Page('pages/manage/manage_location.py', title='Locations'),
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