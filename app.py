import streamlit as st
import json
import os
import pandas as pd

# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:"
    theme=custom_theme
)

# Load the availability status
with open('availability.json', 'r') as f:
    availability = json.load(f)

# Initialize cart
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# Load the last order number if it exists, otherwise initialize it as 0
try:
    with open('last_order_number.txt', 'r') as f:
        last_order_number = int(f.read())
except FileNotFoundError:
    last_order_number = 0

# Main title
with st.container():
    st.markdown("<h1 style='text-align: center; '>Mexitos</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>order online</h2>", unsafe_allow_html=True)
    
with st.container():
    col1,col2 = st.columns([1,1])
    with col1:
        for i, (menu_name, menu) in enumerate(availability.items()):
            col = st.container()
            with col:
                # Create a button to show/hide the checkboxes
                if st.button(f"{menu_name}", key=f"{i}button"):
                    # Toggle the show_options state
                    st.session_state[f"{i}show_options"] = not st.session_state.get(f"{i}show_options", False)

                # If show_options is True, display the checkboxes
                if st.session_state.get(f"{i}show_options", False):
                    # Iterate over menu items
                    for item, item_info in menu.items():
                        if item_info['available']:  # Only display the item if it's available
                            # Create a checkbox for each item
                            selected = st.checkbox(f"{item} ------- {item_info['price']}", key=f"{i}{item}")
                            if selected:
                                # If the checkbox is checked, add a number input for quantity
                                quantity = st.number_input(f"Quantity for {item}", min_value=1, key=f"{i}{item}quantity")
                                # Add the item and quantity to the cart
                                st.session_state['cart'][item] = quantity

# Display the cart
with st.container():
    st.markdown("<h2 style='text-align: center; '>Your Cart</h2>", unsafe_allow_html=True)
    total = 0
    items_to_remove = []
    for item, quantity in st.session_state['cart'].items():
        for menu in availability.values():
            if item in menu:
                price = menu[item]['price']
                # Add a numeric input for quantity in the cart
                quantity = st.number_input(f"Quantity for {item}", min_value=0, value=quantity, key=f"cart{item}quantity")
                if quantity == 0:
                    items_to_remove.append(item)
                else:
                    st.session_state['cart'][item] = quantity
                    total += price * quantity
                st.write(f"{item}: {quantity} x {price} = {quantity * price}")

    # Remove items with quantity 0 from the cart
    for item in items_to_remove:
        del st.session_state['cart'][item]

    # Display the total
    st.write(f"Total: {total}")

# Order Now button
if len(st.session_state['cart']) > 0:
    if st.button('Order Now'):
        # Increment the order number
        last_order_number += 1
        # Save the cart details and order number to an Excel file
        df = pd.DataFrame.from_dict(st.session_state['cart'], orient='index', columns=['Quantity'])
        df.to_excel(f'order_{last_order_number}.xlsx')
        # Save the last order number
        with open('last_order_number.txt', 'w') as f:
            f.write(str(last_order_number))
        st.success(f"Order {last_order_number} has been placed!")
else:
    st.warning("Your cart is empty. Please add items to the cart before placing an order.")
