import streamlit as st
import pandas as pd

csv_file_path = '/home/elijah/beverage/data/raw/'

def main():
    df = pd.read_csv(csv_file_path + "products.csv")

    tea = df[df["product_type_name"] == "Tea"]
    coffee = df[df["product_type_name"] == "Coffee"]
    equipment = df[df["product_type_name"] == "Equipment"]

    tea = tea.reset_index(drop=True)
    coffee = coffee.reset_index(drop=True)
    equipment = equipment.reset_index(drop=True)

    st.title('Product data')

    st.header("Tea")
    tea_cols = ['product_name', 'product_alt_name', 'product_type_name', 'vendor_name',
                'role', 'region','altitude_meters', 'processing_method', 'tea_type',
                'cultivar', 'is_active', 'notes']
    edited_tea = st.data_editor(tea[tea_cols], num_rows="dynamic")
    
    st.write('---')

    st.header("Coffee")
    coffee_cols = ['product_name', 'product_alt_name', 'product_type_name', 'vendor_name',
                   'role', 'region', 'roast_level', 'origin_type', 'varietal', 'altitude_meters', 
                   'processing_method', 'is_active', 'notes']
    edited_coffee = st.data_editor(coffee[coffee_cols], num_rows="dynamic")
    
    st.write('---')

    st.header("Equipment")
    equipment_cols = ['product_name', 'product_alt_name', 'product_type_name', 'vendor_name',
                      'role', 'material', 'volume', 'clay_type', 'pour_speed', 'color', 'is_active',
                      'notes']
    edited_equipment = st.data_editor(equipment[equipment_cols], num_rows="dynamic")

    st.write("---")
    changed = []

    # Compare only the editable columns
    if not edited_tea.equals(tea[tea_cols]):
        changed.append("Tea")
        tea.update(edited_tea)
    if not edited_coffee.equals(coffee[coffee_cols]):
        changed.append("Coffee")
        coffee.update(edited_coffee)
    if not edited_equipment.equals(equipment[equipment_cols]):
        changed.append("Equipment")
        equipment.update(edited_equipment)

    if st.button("Save", use_container_width=True):
        if changed:
            edited_all = pd.concat([tea, coffee, equipment])
            edited_all.to_csv(csv_file_path + "products.csv", index=False)
            st.success(f"Updated: {', '.join(changed)}")
        else:
            st.info("No changes were made")

if __name__ == '__main__':
    main()