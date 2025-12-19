import streamlit as st
import pandas as pd

csv_file_path = '/home/elijah/beverage/data/raw/'

def main():
    st.title('Session data')

    # Load CSV
    df_sessions = pd.read_csv(csv_file_path + 'sessions.csv')
    df_sbi = pd.read_csv(csv_file_path + 'session_batch_inventory.csv')
    df_extractions = pd.read_csv(csv_file_path + 'extractions.csv')

    # Session editor
    st.header('Session')
    edited_sessions = st.data_editor(df_sessions, num_rows="dynamic", use_container_width=True)
    
    st.write('---')

    st.header('Extraction')
    edited_extractions = st.data_editor(df_extractions, num_rows="dynamic", use_container_width=True)

    st.write('---')
    
    st.header('Session Batch Inventory')
    edited_sbi = st.data_editor(df_sbi, num_rows="dynamic", use_container_width=True)

    st.write('---')
    if st.button("Save", use_container_width=True):
        changed = []
        # Detect changes
        if not edited_sessions.equals(df_sessions):
            edited_sessions.to_csv(csv_file_path + 'sessions.csv', index=False)
            changed.append("Sessions")
        if not edited_extractions.equals(df_extractions):
            edited_extractions.to_csv(csv_file_path + 'extractions.csv', index=False)
            changed.append("Extractions")
        if not edited_sbi.equals(df_sbi):
            edited_sbi.to_csv(csv_file_path + 'session_batch_inventory.csv', index=False)
            changed.append("Session Batch Inventory")

        if changed:
            st.success(f"Updated: {', '.join(changed)}")
        else:
            st.info("No changes were made")

    st.write('---')

    st.title('Administration')
    remove_session_code = st.text_input('What session code do you want deleted?')

    if st.button('Delete rows') and remove_session_code:
        missing = []
        total_removed = 0

        for name, df in {
            "sessions.csv": df_sessions,
            "extractions.csv": df_extractions,
            "session_batch_inventory.csv": df_sbi,
        }.items():
            if "session_code" not in df.columns:
                missing.append(name)
                continue

            before = len(df)
            df.drop(df[df["session_code"] == remove_session_code].index, inplace=True)
            removed = before - len(df)
            total_removed += removed

            df.to_csv(csv_file_path + name, index=False)

        if missing:
            st.warning(f"session_code missing in: {', '.join(missing)}")
        elif total_removed == 0:
            st.warning(f"No rows found for session_code = {remove_session_code}")
        else:
            st.success(f"Removed session_code = {remove_session_code} ({total_removed} rows)")

if __name__ == '__main__':
    main()
