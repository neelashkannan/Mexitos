import streamlit as st
import json
import os
import glob
import pandas as pd
import time
import datetime

def generate_order_number():
    return int(time.time())

# Define a function to get the current date and time
def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:"
)

# Define the menu items
menus = {
    "Chicken Dry :chicken:" : {
        "GARLIC CHICKEN": 100,"GINGER CHICKEN": 100,
        "CHINESE CHILLY CHICKEN": 100,
        "SCHEZWAN CHICKEN": 100,
        "CHICKEN MANCHURIAN": 100,
        "DRAGON CHICKEN": 110,
        "PEPPER CHICKEN": 100,
        "CHICKEN 65 ROAST": 110,
        "CHICKEN CHETTINAD": 100,
        "CHICKEN PALLIPALAYAM": 100,
        "CHICKEN 65": 90,
        "EGG CHILLY": 70
    },
    # ... other menus ...
}

# Initialize the availability dictionary
availability = {}

# Load the availability status if it exists
try:
    with open('availability.json', 'r') as f:
        availability = json.load(f)
except json.JSONDecodeError:
    print("Error: JSON file is empty or not properly formatted")
    availability = {menu_name: {item: {'price': price, 'available': True} for item, price in menu.items()} for menu_name, menu in menus.items()}
except FileNotFoundError:
    # If the file doesn't exist, initialize all items as available
    availability = {menu_name: {item: {'price': price, 'available': True} for item, price in menu.items()} for menu_name, menu in menus.items()}
except Exception as e:
    print(f"An error occurred: {e}")
    availability = {menu_name: {item: {'price': price, 'available': True} for item, price in menu.items()} for menu_name, menu in menus.items()}

# Ensure that all items in the menus are in the availability dictionary
for menu_name, menu in menus.items():
    if menu_name not in availability:
        availability[menu_name] = {}
    for item in menu.keys():
        if item not in availability[menu_name]:
            availability[menu_name][item] = {'price': menu[item], 'available': True}

# Create a sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Orders", "Chicken Dry" ])

if page == "Orders":
    # Display the orders
    st.markdown("# Orders")
    order_files = glob.glob('order_*.xlsx')
    for order_file in order_files:
        df = pd.read_excel(order_file, index_col=0)
        st.markdown(f"## Order {order_file.split('_')[1].split('.')[0]}")
        for item, row in df.iterrows():
            st.write(f"{item}: {row['Quantity']}")
        # Add a button to hide the order after delivery
        if st.button(f"Delivered order {order_file.split('_')[1].split('.')[0]}"):
            # Load the existing delivered orders file
            if os.path.exists('delivered_orders.xlsx'):
                df_delivered = pd.read_excel('delivered_orders.xlsx', index_col=0)
            else:
                df_delivered = pd.DataFrame()

            # Append the new order to the delivered orders DataFrame
            df_delivered = df_delivered.append(df)

            # Add the order number and date/time to the DataFrame
            df_delivered['Order Number'] = generate_order_number()
            df_delivered['Date/Time'] = get_current_date_time()

            # Save the updated DataFrame to the Excel file
            df_delivered.to_excel('delivered_orders.xlsx')

            # Delete the original order file
            os.remove(order_file)
            st.rerun()

elif page == "Chicken Dry":
    # Display checkboxes for each item in the "Chicken Dry" menu
    st.markdown(f"## Chicken Dry")
    for item in menus["Chicken Dry :chicken:"]:
        # Create a checkbox for each item
        availability["Chicken Dry :chicken:"][item]['available'] = st.checkbox(f"{item} is available", value=availability["Chicken Dry :chicken:"][item]['available'])
        # Create a number input for each item to display and modify the price
        availability["Chicken Dry :chicken:"][item]['price'] = st.number_input(f"Price for {item}", min_value=0, value=availability["Chicken Dry :chicken:"][item]['price'])

# Save the availability status
with open('availability.json', 'w') as f:
    json.dump(availability, f)
