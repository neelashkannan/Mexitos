import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from chicken_dry_button import display_chicken_dry_button
from bread_items_button import display_bread_items_button
from firebase_data import fetch_chicken_dry_items, fetch_bread_items
from shawarma_button import display_shawarma_button
from rice_button import display_rice_button
from starter_button import display_starter_items_button
import time
import datetime
import json
from biryani_button import display_Biryani_items_button

# Initialize Firebase (same as before)
if not firebase_admin._apps:
    # Initialize Firebase with your credentials
    cred = credentials.Certificate('testing.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://food-or-e1dd3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Get a reference to the Firebase database
ref = db.reference('/')

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Set page title and favicon (same as before)
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:",
    layout="wide"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Get the last order number from Firebase
last_order_number = ref.child('last_order_number').get() or 0
order_number = int(last_order_number) + 1

# Initialize cart and button states (same as before)
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

if 'button_state_chicken_dry' not in st.session_state:
    st.session_state['button_state_chicken_dry'] = False

if 'button_state_bread' not in st.session_state:
    st.session_state['button_state_bread'] = False

if 'button_state_shawarma' not in st.session_state:
    st.session_state['button_state_shawarma'] = False

if 'button_state_rice' not in st.session_state:
    st.session_state['button_state_rice'] = False

if 'button_state_starter' not in st.session_state:
    st.session_state['button_state_starter'] = False

if 'button_state_Biryani' not in st.session_state:
    st.session_state['button_state_Biryani'] = False
# Main title (same as before)
with st.container():
    st.markdown("<h1 style='text-align: center; '>Mexitos</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>order online</h2>", unsafe_allow_html=True)

# Form to enter name and phone number
name = st.text_input("Enter your name:")
phone_number = st.text_input("Enter your phone number:")

# Display Chicken Dry button
display_chicken_dry_button(ref, st.session_state)

# Display Bread Items button
display_bread_items_button(ref, st.session_state)

display_shawarma_button(ref, st.session_state)

display_rice_button(ref, st.session_state)

display_starter_items_button(ref, st.session_state)

display_Biryani_items_button(ref, st.session_state)

# Display the cart and order button (same as before)
with st.container():
    st.markdown("<h2 style='text-align: center; '>Your Cart</h2>", unsafe_allow_html=True)
    total = 0
    order_items = []
    for item_id, quantity in st.session_state['cart'].items():
        if quantity > 0:
            item_data = (ref.child('chicken fry').child(item_id).get() or ref.child('bread_items').child(item_id).get() or ref.child('shawarma').child(item_id).get() or ref.child('rice and noodles items').child(item_id).get()
                        or ref.child('starters').child(item_id).get() or ref.child('Biryani').child(item_id).get())
            if item_data:
                item_name = item_data['item_name']
                item_price = item_data['price']
                quantity_input = st.number_input(f"{item_name} Quantity", min_value=0, max_value=10, value=quantity, key=item_id)
                st.write(f"{item_name}: {quantity_input} x {item_price} = {quantity_input * item_price}")
                order_items.append({'item_id': item_id, 'item_name': item_name, 'quantity': quantity_input, 'price': item_price})
                total += item_price * quantity_input

    # Display the total
    st.write(f"Total: {total}")

# Order button (same as before)
if len(st.session_state['cart']) > 0 and name and phone_number:
    if st.button('Order Now', use_container_width=200):
        # Save the order details, including items, quantities, prices, and order date, to Firebase using the order number as the key
        order_date = get_current_date_time()
        order_data = {'cart': order_items, 'total': total, 'name': name, 'phone_number': phone_number, 'order_date': order_date}
        ref.child('orders').child(str(order_number)).set(order_data)  # Use order number as the key

        # Update the last order number in Firebase
        ref.child('last_order_number').set(order_number)
        #time.sleep(5)
        st.session_state['cart'] = {}

        # Show a success message
        st.success(f"Order placed successfully! Your order number is {order_number}.")

        # Empty the cart after 5 seconds
        
else:
    st.warning("please enter name and phone number to place order")
