#!/home/elijah/beverage/venv/bin/python

import pandas as pd
import numpy
import sys
from pathlib import Path
import shutil

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
