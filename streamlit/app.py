
import os
from datetime import datetime
from pathlib import Path
import streamlit as st
import subprocess
import uuid

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
    if "session_code" not in st.session_state:
        st.session_state["session_code"] = uuid.uuid4()
        
    pg = st.navigation(pages)

    with st.sidebar:
        try:
            ts = float(path.read_text().strip())
            age = (datetime.now().timestamp() - ts) / 60  # minutes
            
            icon = "🟢" if age < 60 else "🟡" if age < 120 else "🔴"
            st.caption(f"{icon} Last sync: {datetime.fromtimestamp(ts):%m/%d %H:%M}")
        except:
            st.caption("🔴 Sync: unknown")


        st.sidebar.caption(f"Session: {str(st.session_state.session_code)[:8]}")

        st.write('----------'   )
        
    # Development utilities
    with st.sidebar.expander("Dev Tools"):
            if st.button("Run Pipeline"):
                with st.spinner("Running..."):
                    try:
                        result = subprocess.run(
                            ["sudo", "-u", "postgres", "/home/elijah/beverage/sql/orchestration/run_all.sh"],
                            capture_output=True,
                            text=True,
                            timeout=300
                        )
                        if result.returncode == 0:
                            st.success("Pipeline completed")
                            st.rerun()
                        else:
                            st.error(f"Failed: {result.stderr}")
                    except Exception as e:
                        st.error(f"Error: {e}")
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