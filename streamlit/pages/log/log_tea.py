# Purpose: This page serves as a CRUD data entry app that reads & writes to csv files to log coffee sessions

# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import uuid
import os
import tempfile
import stat

# Functions
def atomic_write_all(dfs_dict, folder):
    """
    Writes all CSVs atomically: either all are replaced or none

    dfs_dict: dict of {filename: dataframe}
    folder: folder path where CSVs live
    """
    temp_files = {}
    try:
        # write all DataFrames to temp files
        for filename, df in dfs_dict.items():
            tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=folder)
            df.to_csv(tmp.name, index=False)
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp.close()
            temp_files[filename] = tmp.name

        # rename all temp files to actual CSVs
        for filename, tmp_path in temp_files.items():
            target_path = os.path.join(folder, filename)
            os.replace(tmp_path, target_path)
            os.chmod(
                target_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
            )  # 644

    except Exception as e:
        # cleanup any leftover temp files if something failed
        for tmp_path in temp_files.values():
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        raise e


def require_fields(fields: dict, error_prefix="Missing"):
    """Check that fields are not None/empty/0; stops execution if any missing."""
    for name, value in fields.items():
        if value in (None, "", 0):
            st.error(f"**{error_prefix} {name}!**")
            st.stop()


# Session config
session_type = "Tea"
SESSION_CONFIG = {
    "Coffee": {
        "page_title": f"How was your {session_type.lower()}?",
        "brew_methods": (
            "Espresso",
            "Pour Over", 
            "Filter"),
    },
    "Tea": {
        "page_title": f"How was your {session_type.lower()}?",
        "brew_methods": (
            "Western",
            "Gongfu",
            "Grandpa",
            "Kyusu",
            "Cold Brew",
            "Matcha",
        ),
    },
}

config = SESSION_CONFIG[session_type]

# Page config
st.set_page_config(
    page_title="Beverage Web App",
    page_icon=f":{session_type.lower()}:",
    layout="centered",
    initial_sidebar_state="auto",
)

# App config (page-specific)
csv_file_path = "/home/elijah/beverage/data/raw/"
page_title = config["page_title"]

# Dropdown options
water_type_options = ("Filtered", "Tap", "Spring")
location_name_options = ("Quebec Ave", "Mom's")
session_location_name_options = ("House", "Shop", "Outdoors", "Work", "Ceremonial")
brew_methods_options = config["brew_methods"]

# Default options
default_equipment = [
    {"product_name": "Hario 300ml Teapot", "vendor_name": "Amazon"},
    {"product_name": "notNeutral LINO Coffee Mug", "vendor_name": "Eight Ounce Coffee"},
]
default_quantity_used = 18.0 if session_type == "Coffee" else None
default_extraction_number = 1


def main():

    if "tea_product_entries" not in st.session_state:
         st.session_state["tea_product_entries"] = default_equipment.copy()

    if "tea_extraction_entries" not in st.session_state:
        st.session_state["tea_extraction_entries"] = [
            {
                "extraction_number": 1,
                "extraction_time": None,
                "water_temperature": None,
                "quantity_output": None,  # ADD THIS
                "notes": ""
            }
        ]

    # Load csv files
    df_products = pd.read_csv(csv_file_path + "products.csv")
    df_order_items = pd.read_csv(csv_file_path + "order_items.csv")
    df_orders = pd.read_csv(csv_file_path + "orders.csv")
    df_sessions = pd.read_csv(csv_file_path + "sessions.csv")
    df_extractions = pd.read_csv(csv_file_path + "extractions.csv")
    df_session_batch_inventory = pd.read_csv(
        csv_file_path + "session_batch_inventory.csv"
    )

    # Create list of available tea, coffee and equipment
    reference_table = (
        df_order_items.copy()
        .merge(df_orders[["order_number"]], on="order_number", how="left")
        .merge(df_products, on="product_name", how="left")
    )

    # Subset df to
    reference_table = (
        reference_table[
            ["product_name", "product_type_name", "vendor_name", "production_date"]
        ]
        .drop_duplicates()
        .sort_values(
            ["product_type_name", "product_name", "vendor_name", "production_date"]
        )
        .reset_index(drop=True)
        .rename(columns={"product_type_name": "product_type"})
    )

    ingredient_ref_table = (
        reference_table[reference_table["product_type"].isin([session_type])]
        .sort_values(["product_type", "product_name"])
        .drop(columns=["product_type"])
    )
    equip_ref_table = reference_table[
        reference_table["product_type"] == "Equipment"
    ].drop(columns=["production_date", "product_type"])

    ingredient_options = ingredient_ref_table.to_dict("records")
    equip_options = equip_ref_table.to_dict("records")

    # App UI
    st.title(page_title)

    # Ingredient section
    with st.container():
        ingredient = st.selectbox(
            "Coffee",
            options=ingredient_options,
            format_func=lambda x: f'{x["product_name"]} — {x["vendor_name"]} — {x["production_date"]}',
            key="ingredient_entry",
            index=1,
        )

        # Extract values safely
        ing_product_name = ingredient["product_name"]
        ing_vendor_name = ingredient["vendor_name"]
        ing_production_date = ingredient["production_date"]

    # Session section
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            rating = st.number_input(
                "Rating", value=None, min_value=0, step=1, max_value=10,
                key=f"rating_{st.session_state.session_code}"
            )
        
        with col2:
            quantity_in = st.number_input(
                "Tea (g)",
                value=default_quantity_used,
                min_value=0.0,
                max_value=30.0,
                step=0.1,
                format="%0.1f",
                key=f"quantity_in_{st.session_state.session_code}"
            )
        
        with col3:
            brew_method = st.selectbox(
                "Brew Method",
                brew_methods_options,
                placeholder="Select brew method...",
            )

        session_notes = st.text_area("Session Notes", "", height=50, key=f"session_notes_{st.session_state.session_code}")

    # Extractions section (multiple)
    with st.expander("Extractions", icon="🫖", expanded=True):
        
        def add_extraction():
            next_num = len(st.session_state["tea_extraction_entries"]) + 1
            st.session_state["tea_extraction_entries"].append({
                "extraction_number": next_num,
                "extraction_time": None,
                "water_temperature": None,
                "quantity_output": None,  # ADD THIS
                "notes": ""
            })
        
        def remove_extraction():
            if len(st.session_state["tea_extraction_entries"]) > 1:
                st.session_state["tea_extraction_entries"].pop()
        
        for i, extraction in enumerate(st.session_state["tea_extraction_entries"]):
            st.subheader(f"Extraction {i + 1}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                extraction["water_temperature"] = st.number_input(
                    "Temperature", 
                    value=extraction["water_temperature"], 
                    min_value=1, 
                    step=1, 
                    max_value=100,
                    key=f"tea_temp_{i}"
                )
            with col2:
                extraction["extraction_time"] = st.number_input(
                    "Extraction Time", 
                    value=extraction["extraction_time"], 
                    min_value=1, 
                    step=1, 
                    max_value=10000,
                    key=f"tea_time_{i}"
                )
            with col3:
                extraction["quantity_output"] = st.number_input(
                    "Output (g)",
                    value=extraction.get("quantity_output"),
                    min_value=0.1,
                    max_value=1000.0,
                    step=0.1,
                    format="%0.1f",
                    key=f"tea_output_{i}"
                )
            
            extraction["notes"] = st.text_area(
                "Extraction Notes", 
                extraction["notes"], 
                height=50,
                key=f"tea_extraction_notes_{i}"
            )
        
        col1, col2 = st.columns(2)
        col1.button("Add Extraction", on_click=add_extraction, use_container_width=True)
        col2.button("Remove Extraction", on_click=remove_extraction, use_container_width=True)

    # Additional details section
    with st.expander("General details", icon="✏️"):

        # General information section
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                favorite_flag = st.checkbox("Favorite Flag")
                water_type = st.radio("Water Type", water_type_options)

            with col2:
                session_date = st.date_input("Session Date", format="YYYY-MM-DD")
                session_time = st.time_input("Session Time")
                session_datetime = str(session_date) + " " + str(session_time)
                extraction_number = default_extraction_number

            with col3:


                session_location_name = st.selectbox(
                    "Session Location Name", session_location_name_options
                )
                location_name = st.selectbox(
                    "Session Location Name", location_name_options, index=0
                )

    # Equipment section
    with st.expander('Equipment details', icon='⚙️'):

        def add_entry():
             st.session_state["tea_product_entries"].append({"product_name": ""})

        def remove_entry():
            if len( st.session_state["tea_product_entries"]) > 1:  # Keep at least one
                 st.session_state["tea_product_entries"].pop()

        equip_options = [
            {"product_name": "", "vendor_name": ""}
        ] + equip_options  # allow empty value when adding entry

        updated_product_entries = []

        for i, entry in enumerate( st.session_state["tea_product_entries"]):
            idx = next(
                (
                    j
                    for j, e in enumerate(equip_options)
                    if e["product_name"] == entry["product_name"]
                ),
                0,
            )

            equipment_selection = st.selectbox(
                "Equipment",
                options=equip_options,
                index=idx,
                key=f"tea_equipment_{i}",
                format_func=lambda x: (
                    f'{x["product_name"]} — {x["vendor_name"]}'
                    if x["product_name"]
                    else ""
                ),
            )

            updated_product_entries.append(
                {
                    "session_code": st.session_state.session_code,
                    "product_name": equipment_selection["product_name"],
                    "vendor_name": equipment_selection["vendor_name"],
                    "production_date": entry.get("production_date", np.nan),
                    "quantity_used": entry.get("quantity_used", 1),
                    "unit": entry.get("unit", "pcs"),
                }
            )

        st.session_state["tea_product_entries"] = updated_product_entries

        col1, col2 = st.columns(2)
        col1.button("Add Equipment", on_click=add_entry, width="stretch")
        col2.button("Remove Equipment", on_click=remove_entry, width="stretch")

    with st.container():
        # Define new rows that will be inserted
        new_session_row = pd.DataFrame(
            [
                {
                    "session_code":  st.session_state["session_code"],
                    "brewing_method_name": brew_method,
                    "rating": rating,
                    "water_type": water_type,
                    "session_type": session_type,
                    "session_date": session_datetime,
                    "favorite_flag": favorite_flag,
                    "session_location_name": session_location_name,
                    "location_name": location_name,
                    "notes": session_notes,
                }
            ]
        )

        # Create multiple extraction rows
        new_extraction_rows = pd.DataFrame([
            {
                "session_code": st.session_state["session_code"],
                "extraction_number": extraction["extraction_number"],
                "extraction_time": extraction["extraction_time"],
                "water_temperature": extraction["water_temperature"],
                "quantity_output": extraction["quantity_output"], 
                "notes": extraction["notes"],
            }
            for extraction in st.session_state["tea_extraction_entries"]
        ])

        new_ingredient_row = pd.DataFrame(
            [
                {
                    "session_code": st.session_state.session_code,
                    "product_name": ing_product_name,
                    "vendor_name": ing_vendor_name,
                    "production_date": ing_production_date,
                    "quantity_used": quantity_in,
                    "unit": "g",
                }
            ]
        )

        new_equipment_rows = pd.DataFrame.from_records(
             st.session_state["tea_product_entries"],
            columns=[
                "session_code",
                "product_name",
                "vendor_name",
                "production_date",
                "quantity_used",
                "unit",
            ],
        )

        new_sbi_rows = pd.concat([new_ingredient_row, new_equipment_rows])

    # Preview section
    with st.expander("Preview data before saving", icon="🔍"):
        st.subheader("Session Data")
        st.dataframe(new_session_row)

        st.subheader("Extraction Data")
        st.dataframe(new_extraction_rows)

        st.subheader("Session Batch Inventory Data")
        st.dataframe(new_sbi_rows)

    # If button is clicked, adds new rows to csv
    if st.button("Add new rows to csv files", width="stretch", type="primary"):

        # Data quality check before adding rows
        with st.container():

            for i, extraction in enumerate(st.session_state["tea_extraction_entries"]):
                require_fields(
                    {
                        f"extraction {i+1} temperature": extraction["water_temperature"],
                        f"extraction {i+1} time": extraction["extraction_time"],
                        f"extraction {i+1} output": extraction["quantity_output"],  # ADD THIS
                    }
                )

            require_fields(
                {
                    "session_code": st.session_state.session_code,
                    "brewing_method_name": brew_method,
                    "water_type": water_type,
                    "session_type": session_type,
                    "session_date": session_datetime,
                    "session_location_name": session_location_name,
                    "location_name": location_name,
                    "extraction_number": extraction_number,
                    "product_name": ing_product_name,
                    "vendor_name": ing_vendor_name,
                    "production_date": ing_production_date,
                },
                error_prefix="Internal error:",
            )

        # Save section
        with st.container():

            # prepared updated dataframes in memory
            updated_sessions = pd.concat(
                [df_sessions, new_session_row], ignore_index=True
            )
            updated_extractions = pd.concat(
                [df_extractions, new_extraction_rows], ignore_index=True  # Changed from new_extraction_row
            )
            updated_sbi = pd.concat(
                [df_session_batch_inventory, new_sbi_rows], ignore_index=True
            )

            # atomic writes for all 3 csv files
            try:
                atomic_write_all(
                    {
                        "sessions.csv": updated_sessions,
                        "extractions.csv": updated_extractions,
                        "session_batch_inventory.csv": updated_sbi,
                    },
                    csv_file_path,
                )

                # update in-memory DataFrames
                df_sessions = updated_sessions
                df_extractions = updated_extractions
                df_session_batch_inventory = updated_sbi

            except Exception as e:
                st.error(f"Save failed — no files written: {e}")
                st.stop()

        # Session stage variables & rerun
        st.session_state["tea_save_success"] = True
        st.session_state["session_code"] = uuid.uuid4()
        st.session_state["tea_product_entries"] = default_equipment.copy()  # Add this
        st.session_state["tea_extraction_entries"] = [{
            "extraction_number": 1, 
            "extraction_time": None, 
            "water_temperature": None, 
            "quantity_output": None, 
            "notes": ""
        }]
        st.rerun()

    # Show success message if data was saved succesfully
    if st.session_state.get("tea_save_success", False):
        st.success("✅ Successfully saved all brewing data!")
        st.session_state["tea_save_success"] = False


if __name__ == "__main__":
    main()
