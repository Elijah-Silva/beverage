# Title: Beverage Web Application
# Purpose: This application serves as a CRUD data entry app that writes to csv files that tracks my daily drinking sessions

# ~~~~~~~ Script ~~~~~~~~~~

# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import uuid

# Page config
st.set_page_config(page_title='Beverage Web App', page_icon=':tea:', layout='centered', initial_sidebar_state='auto')

# App config
csv_file_path = '/home/elijah/beverage/data/raw'
role_options = ('Accessories', 'Cup', 'Kettle', 'Teapot', 'Gongfu', 'Faircup', 'Espresso Maker')
role_ingredient = 'Tea Dose'
session_type = 'Tea'


@st.cache_data
def load_reference_tables(csv_file_path):
    """Load and prepare reference tables for ingredients and equipment"""
    df_products = pd.read_csv(csv_file_path + '/products.csv')
    df_order_items = pd.read_csv(csv_file_path + '/order_items.csv')
    df_orders = pd.read_csv(csv_file_path + '/orders.csv')
    
    df = df_order_items.merge(
        df_orders[['order_number']], 
        on='order_number', 
        how='left'
    ).merge(
        df_products, 
        on='product_name', 
        how='left'
    )
    
    reference_table = (df[['product_name', 'product_type_name', 'vendor_name', 'production_date']]
                       .drop_duplicates()
                       .sort_values(['product_type_name', 'product_name', 'vendor_name', 'production_date'])
                       .reset_index(drop=True)
                       .rename(columns={'product_name': 'name',
                                        'product_type_name': 'type',
                                        'vendor_name': 'vendor',
                                        'production_date': 'production date'}))
    
    ingredient_ref_table = reference_table[reference_table['type'].isin(['Tea'])].sort_values(['type', 'name']).drop(columns=['type'])
    equip_ref_table = reference_table[reference_table['type'] == 'Equipment'].drop(columns=['production date', 'type'])
    
    return ingredient_ref_table, equip_ref_table

def main():
    st.title('Log Brewed Tea')


    if 'session_code' not in st.session_state:
        st.session_state['session_code'] = uuid.uuid4()

    st.caption(f'Session: {st.session_state.session_code}')

     # Load reference tables (cached)
    ingredient_ref_table, equip_ref_table = load_reference_tables(csv_file_path)


    # Initialize session state CSVs
    for name in ['sessions', 'products', 'session_batch_inventory', 'extractions', 'order_items']:
        if 'name' not in st.session_state:
            st.session_state[name] = pd.read_csv(f'{csv_file_path}/{name}.csv')
        
    # Show success message if data was just saved
    if st.session_state.get('save_success', False):
        st.success('✅ Successfully saved all brewing data!')
        st.session_state['save_success'] = False

    # Ingredient section
    st.subheader('Ingredient Details')

    ingredient_ref_table["display"] = (
        ingredient_ref_table["name"].str.ljust(25)
        + " ------------ "
        + ingredient_ref_table["vendor"].str.ljust(25)
        + " ------------ "
        + ingredient_ref_table["production date"]
    )

    ingredient = st.selectbox(
        "Ingredient",
        ingredient_ref_table["display"].tolist(),
        index=1
    )
    col1, col2 = st.columns(2)


    st.subheader('Session Details')


    col1, col2 = st.columns(2)
    with col1:
        rating = st.number_input('Rating', value=None, min_value=0, step=1, max_value=10)
        grind_size = st.number_input('Grind Size', value=None, min_value=0.1, max_value=30.0, step=0.1, format='%0.1f')
        extraction_time = st.number_input('Extraction Time', value=None, min_value=1, step=1, max_value=10000)

    with col2:
        water_temperature = st.number_input('Water Temperature', value=None, min_value=1, step=1, max_value=100)
        quantity_in = st.number_input('Quantity Used', value=18.0, min_value=0.0, max_value=30.0, step=0.1, format='%0.1f')
        quantity_output = st.number_input('Quantity Out', value=None, min_value=0.1, max_value=1000.0, step=0.1, format='%0.1f')

    session_notes = st.text_area('Session Notes', '', height=50)
    extraction_notes = ''

    with st.expander('Edit additional details', icon='✏️'):
        
        st.subheader('General Information')

        col1, col2 = st.columns(2)
        with col1:
            favorite_flag = st.checkbox('Favorite Flag')
            water_type = st.radio(
                'Water Type',
                ('Filtered', 'Tap', 'Spring'),
            )

            brew_method = st.selectbox(
                'Brew Method',
                ('Espresso', 'Western', 'Gongfu', 'Grandpa', 'Kyusu', 'Cold Brew', 'Matcha', 'Filter', 'Moka', 'Pour Over'),
                placeholder='Select brew method...',
            )

            extraction_number = 1

        with col2:
            session_date = st.date_input('Session Date', format='YYYY-MM-DD')
            session_time = st.time_input('Session Time')
            session_datetime = str(session_date) + ' ' + str(session_time)
            session_location_name = st.selectbox(
                'Session Location Name',
                ('House', 'Shop', 'Outdoors', 'Work', 'Ceremonial'),
            )
            location_name = st.selectbox(
                'Session Location Name',
                ('Quebec Ave', 'Mom\'s'),
                index=0
            )

            product_name, vendor_name, production_date = ingredient.split(" ------------ ")

            new_ingredient_rows = pd.DataFrame([{
                "session_code": st.session_state.session_code,
                "product_name": product_name,
                "vendor_name": vendor_name,
                "production_date": production_date,
                "quantity_used": quantity_in,
                "quantity_output": quantity_output,
                "role": role_ingredient,
                "unit": "g",
            }])

        # Equipment section
        st.subheader('Equipment')

        with st.expander('Show current equipment:'):
            st.write(equip_ref_table)

        if 'entries' not in st.session_state:
            st.session_state.entries = [
                {"product_name": "Cafelat Robot", "vendor_name": "Cafune", "role": "Espresso Maker"},
                {"product_name": "Robot Paper Filters", "vendor_name": "Cafune", "role": "Accessories"},
                {"product_name": "Subminimal Flick WDT Tool", "vendor_name": "Cafune", "role": "Accessories"},
                {"product_name": "notNeutral VERO Espresso Glass", "vendor_name": "Eight Ounce Coffee",
                    "role": "Cup"}
            ]

        def add_entry():
            st.session_state.entries.append({
                'product_name': 'Cafelat Robot',
                'vendor_name': 'Cafune',
                'role': 'Espresso Maker'
            })

        def remove_entry():
            if len(st.session_state.entries) > 1:  # Keep at least one
                st.session_state.entries.pop()

        # --- Dynamic input rows ---
        tbl = equip_ref_table
        product_options = tbl['name'].unique().tolist()
        vendor_options = tbl['vendor'].unique().tolist()
        for i, entry in enumerate(st.session_state.entries):
            st.markdown(f'##### Item {i + 1} - {entry["product_name"]}')

            col1, col2, col3 = st.columns(3)

            with col1:
                entry['product_name'] = st.selectbox(
                    'Product Name',
                    product_options,
                    index=product_options.index(entry['product_name']),
                    key=f'product_{i}'
                )

            with col2:
                entry['vendor_name'] = st.selectbox(
                    'Vendor Name',
                    vendor_options,
                    index=vendor_options.index(entry['vendor_name']),
                    key=f'vendor_{i}'
                )

            with col3:
                entry['role'] = st.selectbox(
                    'Role',
                    role_options,
                    index=role_options.index(entry['role']),
                    key=f'role_{i}'
                )

        new_equipment_rows = pd.DataFrame(st.session_state.entries)

        # insert first column at position 0
        new_equipment_rows.insert(0, 'session_code', st.session_state.session_code,)

        # rest of columns
        new_equipment_rows['production_date'] = np.nan
        new_equipment_rows['quantity_used'] = 1
        new_equipment_rows['quantity_output'] = np.nan
        new_equipment_rows['unit'] = 'pcs'

        # optionally reorder columns
        cols_order = [
            'session_code', 'product_name', 'vendor_name', 'production_date',
            'quantity_used', 'quantity_output', 'unit', 'role'
        ]

        new_equipment_rows = new_equipment_rows.reindex(columns=cols_order)
        new_sbi_rows = pd.concat([new_ingredient_rows, new_equipment_rows])
        
        # Add button
        col1, col2 = st.columns(2)

        with col1:
            st.button('Add Equipment', on_click=add_entry, width='stretch')

        with col2:
            st.button('Remove Equipment', on_click=remove_entry, width='stretch')

    # Add preview section
    with st.expander('Preview data before saving', icon='🔍'):
        st.subheader('Session Data')
        preview_session = pd.DataFrame([[st.session_state['session_code'],
                                        brew_method, rating, water_type, session_type,
                                        session_datetime, favorite_flag, session_location_name,
                                        location_name, grind_size, session_notes]],
                                    columns=st.session_state['sessions'].columns,)
        st.dataframe(preview_session)
        
        st.subheader('Extraction Data')
        preview_extraction = pd.DataFrame([[st.session_state['session_code'],
                                            extraction_number, extraction_time, 
                                            water_temperature, extraction_notes]],
                                        columns=st.session_state['extractions'].columns)
        st.dataframe(preview_extraction)
        
        st.subheader('Session Batch Inventory Data')
        st.dataframe(new_sbi_rows)

    if st.button('Add new rows to csv(s)', width='stretch', type='primary'):

        # Data quality check before adding rows
        required_session = {
            'brew method': brew_method,
            'rating': rating,
            'water type': water_type,
            'session type': session_type,
            'session datetime': session_datetime,
            'favorite flag': favorite_flag,
            'session location name': session_location_name,
            'location name': location_name,
        }
        missing_session_data = [k for k, v in required_session.items() if v is None]

        required_extraction = {
            'extraction number': extraction_number,
            'extraction time': extraction_time,
            'water temperature': water_temperature,
        }
        missing_extraction_data = [k for k, v in required_extraction.items() if v is None]

        if rating == 0:
            st.error(f'**Missing rating!**')
            st.stop()

        if grind_size is None:
            st.error(f'**Missing grind size!**')
            st.stop()

        if quantity_output is None:
            st.error(f'**Missing quantity out!**')
            st.stop()

        if missing_session_data:
            st.error(f'**Missing session data:** {", ".join(missing_session_data)}')
            st.stop()

        if missing_extraction_data:
            st.error(f'**Missing extractions data:** {", ".join(missing_extraction_data)}')
            st.stop()

        # Save sessions
        try:
            # Create the new row
            new_session_row = pd.DataFrame([[st.session_state['session_code'],
                                            *required_session.values(),
                                            grind_size,
                                            session_notes]],
                                        columns=st.session_state['sessions'].columns)
            
            # Combine into updated dataframe
            updated_sessions = pd.concat([st.session_state['sessions'], new_session_row], ignore_index=True)
            
            # Write to CSV first
            updated_sessions.to_csv(f'{csv_file_path}/sessions.csv', index=False)
            
            # Only update session state if write succeeded
            st.session_state['sessions'] = updated_sessions
            
        except Exception as e:
            st.error(f'Failed to save sessions: {e}')
            st.stop()

        # Save extractions
        try:
            new_extraction_row = pd.DataFrame([[st.session_state['session_code'],
                                                *required_extraction.values(),
                                                extraction_notes]],
                                            columns=st.session_state['extractions'].columns)
            
            updated_extractions = pd.concat([st.session_state['extractions'], new_extraction_row], ignore_index=True)
            
            updated_extractions.to_csv(f'{csv_file_path}/extractions.csv', index=False)
            
            st.session_state['extractions'] = updated_extractions
            
        except Exception as e:
            st.error(f'Failed to save extractions: {e}')
            st.stop()

        # Save session batch inventory
        try:
            updated_sbi = pd.concat([st.session_state['session_batch_inventory'], new_sbi_rows], ignore_index=True)
            
            updated_sbi.to_csv(f'{csv_file_path}/session_batch_inventory.csv', index=False)
            
            st.session_state['session_batch_inventory'] = updated_sbi
            
        except Exception as e:
            st.error(f'Failed to save session batch inventory: {e}')
            st.stop()

        st.session_state['save_success'] = True
        st.session_state['session_code'] = uuid.uuid4()
        st.rerun()

if __name__ == '__main__':
    main()
