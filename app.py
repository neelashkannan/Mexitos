import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase
if not firebase_admin._apps:
    # Initialize Firebase with your credentials
    cred = credentials.Certificate('C:\\Users\\Robonium\\Desktop\\OneDrive\\Documents\\codes\\food ordering\\testing.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://food-or-e1dd3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Get a reference to the Firebase database
ref = db.reference('/')

# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:"
)

order_number = int(time.time())
# Fetch the "chicken fry" section from Firebase
chicken_dry_items = ref.child('chicken fry').get()
bread_items = ref.child('bread_items').get()  # Changed to 'bread_items'

# Initialize cart
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# Initialize checkbox state dictionary for Chicken Dry
if 'checkbox_state_chicken_dry' not in st.session_state:
    st.session_state['checkbox_state_chicken_dry'] = {}

# Initialize checkbox state dictionary for Bread Items
if 'checkbox_state_bread' not in st.session_state:
    st.session_state['checkbox_state_bread'] = {}

# Initialize button state for Chicken Dry
if 'button_state_chicken_dry' not in st.session_state:
    st.session_state['button_state_chicken_dry'] = False

# Initialize button state for Bread Items
if 'button_state_bread' not in st.session_state:
    st.session_state['button_state_bread'] = False

# Main title
with st.container():
    st.markdown("<h1 style='text-align: center; '>Mexitos</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>order online</h2>", unsafe_allow_html=True)

# Toggle button for "Chicken Fry"
if st.button("Chicken Fry :chicken:"):
    st.session_state['button_state_chicken_dry'] = not st.session_state.get('button_state_chicken_dry', False)

# Display available items from "chicken fry" if button is toggled on
if st.session_state.get('button_state_chicken_dry', False):
    with st.container():
        for item_id, item_data in chicken_dry_items.items():
            if item_data.get('available', False):  # Check if the item is available
                # Get the checkbox state from session state for Chicken Dry
                checkbox_state_chicken_dry = st.session_state['checkbox_state_chicken_dry'].get(item_id, False)
                # Create a checkbox for each available item in Chicken Dry
                selected_chicken_dry = st.checkbox(f"{item_data['item_name']} ------- {item_data['price']}",
                                                    value=checkbox_state_chicken_dry)
                # Update checkbox state in session state for Chicken Dry
                st.session_state['checkbox_state_chicken_dry'][item_id] = selected_chicken_dry
                if selected_chicken_dry:
                    # If the checkbox is checked, add a number input for quantity
                    quantity_chicken_dry = st.session_state['cart'].get(item_data['item_name'], {}).get('quantity', 1)
                    quantity_chicken_dry = st.number_input(f"Quantity for {item_data['item_name']}",
                                                           min_value=1, value=quantity_chicken_dry)
                    # Add the item, price, and quantity to the cart for Chicken Dry
                    st.session_state['cart'][item_data['item_name']] = {'quantity': quantity_chicken_dry,
                                                                        'price': item_data['price']}

# Toggle button for "Bread Items"
if st.button("Bread Items :bread:"):
    st.session_state['button_state_bread'] = not st.session_state.get('button_state_bread', False)

# Display available items from "bread_items" if button is toggled on
if st.session_state.get('button_state_bread', False) and bread_items is not None:
    with st.container():
        for item_id, item_data in bread_items.items():
            if item_data.get('available', False):  # Check if the item is available
                # Get the checkbox state from session state for Bread Items
                checkbox_state_bread = st.session_state['checkbox_state_bread'].get(item_id, False)
                # Create a checkbox for each available item in Bread Items
                selected_bread = st.checkbox(f"{item_data['item_name']} ------- {item_data['price']}",
                                             value=checkbox_state_bread)
                # Update checkbox state in session state for Bread Items
                st.session_state['checkbox_state_bread'][item_id] = selected_bread
                if selected_bread:
                    # If the checkbox is checked, add a number input for quantity
                    quantity_bread = st.session_state['cart'].get(item_data['item_name'], {}).get('quantity', 1)
                    quantity_bread = st.number_input(f"Quantity for {item_data['item_name']}",
                                                     min_value=1, value=quantity_bread)
                    # Add the item, price, and quantity to the cart for Bread Items
                    st.session_state['cart'][item_data['item_name']] = {'quantity': quantity_bread,
                                                                        'price': item_data['price']}

# Display the cart and order button
with st.container():
    st.markdown("<h2 style='text-align: center; '>Your Cart</h2>", unsafe_allow_html=True)
    total = 0
    items_to_remove = []
    for item, item_data in st.session_state['cart'].items():
        price = item_data['price']
        quantity = item_data['quantity']
        # Add a numeric input for quantity in the cart
        quantity = st.number_input(f"Quantity for {item}", min_value=0, value=quantity, key=f"cart{item}quantity")
        if quantity == 0:
            items_to_remove.append(item)
        else:
            st.session_state['cart'][item]['quantity'] = quantity
            total += price * quantity
        st.write(f"{item}: {quantity} x {price} = {quantity * price}")

    # Remove items with quantity 0 from the cart
    for item in items_to_remove:
        del st.session_state['cart'][item]

    # Display the total
    st.write(f"Total: {total}")

last_order_number = ref.child('last_order_number').get()
if last_order_number is None:
    last_order_number = 0  # Set default last order number if it doesn't exist yet

# Generate the next order number by incrementing the last order number
order_number = last_order_number + 1

if len(st.session_state['cart']) > 0:
    if st.button('Order Now'):
        # Generate the next order number by incrementing the last order number
        last_order_number = ref.child('last_order_number').get()
        if last_order_number is None:
            last_order_number = 0  # Set default last order number if it doesn't exist yet
        order_number = last_order_number + 1

        # Save the cart details, price, and total to Firebase using the order number as the key
        order_data = {'cart': st.session_state['cart'], 'total': total}
        ref.child('orders').child(str(order_number)).set(order_data)  # Use order number as the key

        # Update the last order number in Firebase
        ref.child('last_order_number').set(order_number)

        # Show a success message
        st.success(f"Order placed successfully! Your order number is {order_number}.")
