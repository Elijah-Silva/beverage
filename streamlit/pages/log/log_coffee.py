# Purpose: This page serves as a CRUD data entry app that reads & writes to csv files to log coffee sessions

# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import uuid

# Page config
st.set_page_config(
    page_title='Beverage Web App', 
    page_icon=':coffee:', 
    layout='centered', 
    initial_sidebar_state='auto'
)

# App config (page-specific)
csv_file_path = '/home/elijah/beverage/data/raw/'
session_type = 'Coffee'
page_title = 'Log coffee'

# Dropdown options
water_type_options = ('Filtered', 'Tap', 'Spring')
location_name_options = ('Quebec Ave', 'Mom\'s')
session_location_name_options = ('House', 'Shop', 'Outdoors', 'Work', 'Ceremonial')
brew_methods_options = ('Espresso', 'Pour Over', 'Filter') # for Tea page: 'Western', 'Gongfu', 'Grandpa', 'Kyusu', 'Cold Brew', 'Matcha','Moka'

# Default options
default_equipment = [
    {"product_name": "Cafelat Robot", "vendor_name": "Cafune"},
    {"product_name": "Robot Paper Filters", "vendor_name": "Cafune"},
    {"product_name": "Subminimal Flick WDT Tool", "vendor_name": "Cafune"},
    {"product_name": "notNeutral VERO Espresso Glass", "vendor_name": "Eight Ounce Coffee"},
]
default_quantity_used = 18.0
default_extraction_number = 1

def main():
    # Initiliaze session state variables
    if 'session_code' not in st.session_state:
        st.session_state['session_code'] = uuid.uuid4()

    if "product_entries" not in st.session_state:
        st.session_state.product_entries = default_equipment.copy()

    st.sidebar.caption(f'Session: {st.session_state.session_code}')

    # Load csv files
    df_products = pd.read_csv(csv_file_path + 'products.csv')
    df_order_items = pd.read_csv(csv_file_path + 'order_items.csv')
    df_orders = pd.read_csv(csv_file_path + 'orders.csv')
    df_sessions = pd.read_csv(csv_file_path + 'sessions.csv')
    df_extractions = pd.read_csv(csv_file_path + 'extractions.csv')
    df_session_batch_inventory = pd.read_csv(csv_file_path + 'session_batch_inventory.csv')

    # Create list of available tea, coffee and equipment
    reference_table = df_order_items.copy() \
        .merge(df_orders[['order_number']], on='order_number',  how='left') \
        .merge(df_products, on='product_name', how='left')

    # Subset df to
    reference_table = reference_table[['product_name', 'product_type_name', 'vendor_name', 'production_date']] \
        .drop_duplicates() \
        .sort_values(['product_type_name', 'product_name', 'vendor_name', 'production_date']) \
        .reset_index(drop=True) \
        .rename(columns={'product_type_name': 'product_type'})
    
    ingredient_ref_table = reference_table[reference_table['product_type'].isin([session_type])].sort_values(['product_type', 'product_name']).drop(columns=['product_type'])
    equip_ref_table = reference_table[reference_table['product_type'] == 'Equipment'].drop(columns=['production_date', 'product_type'])

    ingredient_options = [
        {"product_name": row["product_name"], "vendor_name": row["vendor_name"], "production_date": row["production_date"]}
        for _, row in ingredient_ref_table.iterrows()
        ]
    
    equip_options = [
        {"product_name": row["product_name"], "vendor_name": row["vendor_name"]}
        for _, row in equip_ref_table.iterrows()
        ]

    # App UI
    st.title(page_title)

    # Ingredient section
    with st.container():
        st.subheader('Ingredient Details')

        ingredient = st.selectbox(
            "What coffee did you use?",
            options=ingredient_options,
            format_func=lambda x: f'{x["product_name"]} — {x["vendor_name"]} — {x["production_date"]}',
            key='ingredient_entry',
            index=1
        )

        # Extract values safely
        ing_product_name = ingredient["product_name"]
        ing_vendor_name = ingredient["vendor_name"]
        ing_production_date = ingredient["production_date"]

    # Session section
    with st.container():
        st.subheader('Session Details')

        col1, col2 = st.columns(2)
        with col1:
            rating = st.number_input('Rating', value=None, min_value=0, step=1, max_value=10)
            grind_size = st.number_input('Grind Size', value=None, min_value=0.1, max_value=30.0, step=0.1, format='%0.1f')
            extraction_time = st.number_input('Extraction Time', value=None, min_value=1, step=1, max_value=10000)

        with col2:
            water_temperature = st.number_input('Water Temperature', value=None, min_value=1, step=1, max_value=100)
            quantity_in = st.number_input('Quantity Used', value=default_quantity_used, min_value=0.0, max_value=30.0, step=0.1, format='%0.1f')
            quantity_output = st.number_input('Quantity Out', value=None, min_value=0.1, max_value=1000.0, step=0.1, format='%0.1f')

        session_notes = st.text_area('Session Notes', '', height=50)
        extraction_notes = ''

    # Additional details section
    with st.expander('Edit additional details', icon='✏️'):        
        
        # General information section
        with st.container():
            st.subheader('General Information')

            col1, col2 = st.columns(2)
            with col1:
                favorite_flag = st.checkbox('Favorite Flag')
                water_type = st.radio('Water Type', water_type_options)
                brew_method = st.selectbox('Brew Method', brew_methods_options, placeholder='Select brew method...')
                extraction_number = default_extraction_number

            with col2:
                session_date = st.date_input('Session Date', format='YYYY-MM-DD')
                session_time = st.time_input('Session Time')
                session_datetime = str(session_date) + ' ' + str(session_time)
                session_location_name = st.selectbox('Session Location Name', session_location_name_options)
                location_name = st.selectbox('Session Location Name', location_name_options, index=0)
        
        # Equipment section
        with st.container():
            st.subheader('Equipment')

            def add_entry():
                st.session_state.product_entries.append({"product_name": ""})

            def remove_entry():
                if len(st.session_state.product_entries) > 1:  # Keep at least one
                    st.session_state.product_entries.pop()
                    
            equip_options = [{"product_name": "", "vendor_name": ""}] + equip_options  # allow empty value when adding entry
            
            for i, entry in enumerate(st.session_state.product_entries):
                idx = next((j for j, e in enumerate(equip_options) if e["product_name"] == entry["product_name"]), 0)

                equipment_selection = st.selectbox(
                    "Equipment",
                    options=equip_options,
                    index=idx,
                    key=f"equipment_{i}",
                    format_func=lambda x: f'{x["product_name"]} — {x["vendor_name"]}' if x["product_name"] else ""
                )

                st.session_state.product_entries[i] = {
                    "session_code": st.session_state.session_code,
                    "product_name": equipment_selection["product_name"],
                    "vendor_name": equipment_selection["vendor_name"],
                    "production_date": entry.get("production_date", np.nan),
                    "quantity_used": entry.get("quantity_used", 1),
                    "quantity_output": entry.get("quantity_output", np.nan),
                    "unit": entry.get("unit", "pcs"),
                }

            col1, col2 = st.columns(2)
            col1.button('Add Equipment', on_click=add_entry, width='stretch')
            col2.button('Remove Equipment', on_click=remove_entry, width='stretch')

        # Define required dicts for validation/abstraction
        new_session_row = pd.DataFrame([{
            'session_code': st.session_state['session_code'],
            'brewing_method_name': brew_method,
            'rating': rating,
            'water_type': water_type,
            'session_type': session_type,
            'session_date': session_datetime,
            'favorite_flag': favorite_flag,
            'session_location_name': session_location_name,
            'location_name': location_name,
            "grind_size": grind_size,
            "notes": session_notes
        }])

        new_extraction_row = pd.DataFrame([{
            'session_code': st.session_state['session_code'],
            'extraction_number': extraction_number,
            'extraction_time': extraction_time,
            'water_temperature': water_temperature,
            "notes": extraction_notes,
        }])

        new_ingredient_row = pd.DataFrame([{
            "session_code": st.session_state.session_code,
            "product_name": ing_product_name,
            "vendor_name": ing_vendor_name,
            "production_date": ing_production_date,
            "quantity_used": quantity_in,
            "quantity_output": quantity_output,
            "unit": "g",
        }])

        new_equipment_rows = pd.DataFrame.from_records(
            st.session_state.product_entries,
            columns=[
                "session_code",
                "product_name",
                "vendor_name",
                "production_date",
                "quantity_used",
                "quantity_output",
                "unit",
            ],
        )

        new_sbi_rows = pd.concat([new_ingredient_row, new_equipment_rows])

    # Preview section
    with st.expander('Preview data before saving', icon='🔍'):
        st.subheader('Session Data')
        st.dataframe(new_session_row)

        st.subheader('Extraction Data')
        st.dataframe(new_extraction_row)

        st.subheader('Session Batch Inventory Data')
        st.dataframe(new_sbi_rows)

    # If button is clicked, adds new rows to csv
    if st.button('Add new rows to csv files', width='stretch', type='primary'):
        
        # Data quality check before adding rows
        with st.container(): 

            #### CREATE DATA QUALITY CHECK TO MAKE SURE ALL ROWS ARE INPUTED

            # Check other required fields
            if rating in (None, 0):
                st.error("**Missing rating!**")
                st.stop()

            if grind_size in (None, ""):
                st.error("**Missing grind size!**")
                st.stop()

            if quantity_output in (None, ""):
                st.error("**Missing quantity out!**")
                st.stop()

        # Save section
        with st.container():
            # Save sessions

            try:
                updated_sessions = pd.concat([df_sessions, new_session_row], ignore_index=True)
                updated_sessions.to_csv(csv_file_path + 'sessions.csv', index=False)
                df_sessions = updated_sessions
                
            except Exception as e:
                st.error(f'Failed to save sessions: {e}')
                st.stop()

            # Save extractions
            try:
                updated_extractions = pd.concat([df_extractions, new_extraction_row], ignore_index=True)
                updated_extractions.to_csv(csv_file_path + 'extractions.csv', index=False)
                df_extractions = updated_extractions
                
            except Exception as e:
                st.error(f'Failed to save extractions: {e}')
                st.stop()

            # Save session batch inventory
            try:
                updated_sbi = pd.concat([df_session_batch_inventory, new_sbi_rows], ignore_index=True)
                updated_sbi.to_csv(csv_file_path + 'session_batch_inventory.csv', index=False)
                df_session_batch_inventory = updated_sbi
                
            except Exception as e:
                st.error(f'Failed to save session batch inventory: {e}')
                st.stop()

        # Session stage variables & rerun
        st.session_state['save_success'] = True
        st.session_state['session_code'] = uuid.uuid4()
        st.rerun()
    
    # Show success message if data was saved succesfully
    if st.session_state.get('save_success', False):
        st.success('✅ Successfully saved all brewing data!')
        st.session_state['save_success'] = False

if __name__ == '__main__':
    main()