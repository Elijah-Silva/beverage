import streamlit as st

pages = {
    "Create new entry": [
        st.Page('create_coffee.py', title='Log coffee'),
        st.Page('create_tea.py', title='Log tea'),
    ],
    "Administration": [
        st.Page('manage_sessions.py', title='Manage sessions'),
        st.Page('manage_extractions.py', title='Manage extractions'),
        st.Page('manage_product.py', title='Manage products'),
        st.Page('manage_vendor.py', title='Manage vendors'),
        st.Page('manage_order.py', title='Manage orders'),
        st.Page('manage_location.py', title='Manage locations'),
    ],
}

pg = st.navigation(pages)
pg.run()
