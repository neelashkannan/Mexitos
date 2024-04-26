import time
import datetime
import json
import streamlit as st

import firebase_admin
from firebase_admin import credentials, db
from firebase_data import fetch_chicken_dry_items, fetch_bread_items

from button.chicken_dry_button import display_chicken_dry_button
from button.bread_items_button import display_bread_items_button
from button.shawarma_button import display_shawarma_button
from button.rice_button import display_rice_button
from button.starter_button import display_starter_items_button
from button.biryani_button import display_Biryani_items_button


from Policy.terms_and_conditions import get_terms_and_conditions
from Policy.privacy_policy import get_privacy_policy
from Policy.return_and_refund_policy import get_return_and_refund_policy

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('testing.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://food-or-e1dd3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Get a reference to the Firebase database
ref = db.reference('/')

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

default_keys = {
    'cart': {},
    'button_state_chicken_dry': False,
    'button_state_bread': False,
    'button_state_shawarma': False,
    'button_state_rice': False,
    'button_state_starter': False,
    'button_state_Biryani': False,
    'selected_section': None,
}

for key, default_value in default_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Set page title and favicon
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




# Display the main content for ordering online
st.markdown("<h1 style='text-align: center; '>Welcome to Mexitos</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; '>Order Online</h2>", unsafe_allow_html=True)

# Form to enter name and phone number
name = st.text_input("Enter your name:")
phone_number = st.text_input("Enter your phone number:")

# Display Chicken Dry button
display_chicken_dry_button(ref, st.session_state)
display_bread_items_button(ref, st.session_state)
display_shawarma_button(ref, st.session_state)
display_rice_button(ref, st.session_state)
display_starter_items_button(ref, st.session_state)
display_Biryani_items_button(ref, st.session_state)

    
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

      
        st.write(f"Total: {total}")
    
    
try:
        last_order_number = ref.child('last_order_number').get()
        if last_order_number is None:
            last_order_number = 0  
        order_number = int(last_order_number) + 1
except Exception as e:
        st.error(f"Error fetching order number: {e}")
        order_number = 1  

if 'cart' not in st.session_state:
        st.session_state['cart'] = {}

st.write(f"Current order number: {order_number}")

if st.button("Place Order"):
        order_data = {
            'order_number': order_number,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # other order details
        }
        ref.child('orders').child(str(order_number)).set(order_data)
        ref.child('last_order_number').set(order_number)
        st.success(f"Order placed successfully! Your order number is {order_number}.")

else:
        st.warning("Please enter your name and phone number to place an order.")


st.markdown("---")  

if st.button("Terms and Conditions"):
    st.session_state["selected_section"] = "Terms and Conditions"

if st.button("Privacy Policy"):
    st.session_state["selected_section"] = "Privacy Policy"

if st.button("Return and Refund Policy"):
    st.session_state["selected_section"] = "Return and Refund Policy"

if st.session_state["selected_section"] == "Terms and Conditions":
    st.markdown(get_terms_and_conditions(), unsafe_allow_html=True)

elif st.session_state["selected_section"] == "Privacy Policy":
    st.markdown(get_privacy_policy(), unsafe_allow_html=True)

elif st.session_state["selected_section"] == "Return and Refund Policy":
    st.markdown(get_return_and_refund_policy(), unsafe_allow_html=True)
