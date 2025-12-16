import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import shutil

st.set_page_config(layout="wide")

csv_file_path = Path('/home/elijah/beverage/data/raw')

df_sessions = pd.read_csv(csv_file_path / 'sessions.csv')
df_sbi = pd.read_csv(csv_file_path / 'session_batch_inventory.csv')
df_extractions = pd.read_csv(csv_file_path / 'extractions.csv')

def main():
    with st.expander('Delete session rows from session, extraction and session batch inventory'):
        remove_session_code = st.text_input('Session code to remove:')

        if st.button('Delete') and remove_session_code:
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

                df.to_csv(csv_file_path / name, index=False)
                print(f"{name}: removed {removed} rows")

            if missing:
                st.warning(f"session_code missing in: {', '.join(missing)}")
            elif total_removed == 0:
                st.warning(f"No rows found for session_code = {remove_session_code}")
            else:
                st.success(f"Removed session_code = {remove_session_code} ({total_removed} rows)")

    st.header('Session data')
    st.data_editor(df_sessions)

    st.header('Extraction data')      
    st.data_editor(df_extractions)

    st.header('Session batch inventory data')
    st.data_editor(df_sbi) 


if __name__ == '__main__':
    main()

if False:
    uuid_to_remove = sys.argv[1]
    raw_path = Path('/home/elijah/beverage/data/raw')

    dfs = {
        "sessions.csv": pd.read_csv(raw_path / "sessions.csv"),
        "extractions.csv": pd.read_csv(raw_path / "extractions.csv"),
        "session_batch_inventory.csv": pd.read_csv(raw_path / "session_batch_inventory.csv"),
    }

    for name, df in dfs.items():
        if 'session_code' in df.columns:
            # backup
            shutil.copy(raw_path / name, raw_path / f"{name}.bak")
            
            # remove rows
            before = len(df)
            df = df[df['session_code'] != uuid_to_remove]
            after = len(df)
            
            # write back
            df.to_csv(raw_path / name, index=False)
            
            # log
            print(f"{name}: removed {before - after} rows")