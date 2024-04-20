import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import time
import datetime

def generate_order_number():
    return int(time.time())

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
food_items = {
    "GARLIC CHICKEN": 100,
    "GINGER CHICKEN": 100,
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
}
# Initialize Firebase
if not firebase_admin._apps:
    # Initialize Firebase with your credentials
    cred = credentials.Certificate('testing.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://food-or-e1dd3-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Get a reference to the Firebase database
ref = firebase_db.reference('/')
availability_ref = ref.child('availability').child('Chicken Dry :chicken:')
availability = availability_ref.get()
# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:"
)

# Create a sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Orders", "Chicken Dry","Bread Items"])

if page == "Orders":
    st.markdown("# Orders")
    orders_data = ref.child('orders').get()
    if orders_data:
        for order_number, order_data in orders_data.items():
            st.markdown(f"## Order {order_number}")
            cart = order_data.get('cart')
            total = order_data.get('total')
            if cart is not None and total is not None:
                items_table = "| Item | Quantity | Price | Total |\n|---|---|---|---|\n"
                order_total = 0
                for item, item_data in cart.items():
                    item_quantity = item_data.get('quantity', 0)
                    item_price = item_data.get('price', 0)
                    item_total = item_quantity * item_price
                    items_table += f"| {item} | {item_quantity} | {item_price} | {item_total} |\n"
                    order_total += item_total
                
                items_table += f"| **Total Order Amount:** | | | {order_total} |\n"
                st.markdown(items_table, unsafe_allow_html=True)

                if st.button(f"Mark Order {order_number} as Delivered"):
                    delivered_orders_ref = ref.child('delivered_orders')
                    delivered_orders_ref.push(order_data)
                    ref.child('orders').child(order_number).delete()
                    st.success(f"Order {order_number} marked as delivered and removed from current orders!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning(f"Order {order_number} data is incomplete or unavailable.")

elif page == "Chicken Dry":
    st.markdown(f"## Chicken Dry Menu")

    existing_items = ref.child('chicken fry').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1,col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('chicken fry').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                trashbin_img = ":wastebasket:"
                #trashbin_url = f"https://emojicombos.com/wp-content/uploads/Trashbin-Emoji-{trashbin_img}.png"
                #st.image(trashbin_url, width=24)
                if delete_item:
                    ref.child('chicken fry').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Add new item form
    st.markdown("### Add New Food Item")
    new_item = st.text_input("Enter Food Item")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add Item"):
        if new_item and price:
            # Save new item to Firebase under 'Chicken Fry'
            new_item_ref = ref.child('chicken fry').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New item added successfully!")
            # Refresh the page after adding new item
            st.experimental_rerun()
        else:
            st.warning("Please enter both the food item and price.")

elif page == "Bread Items":
    st.markdown("## Bread Items Menu")

    existing_items = ref.child('bread_items').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1,col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"bread_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('bread_items').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.experimental_rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('bread_items').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.experimental_rerun()

    # Add new item form for Bread Items
    st.markdown("### Add New Bread Item")
    new_item = st.text_input("Enter Bread Item")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add Bread Item"):
        if new_item and price:
            # Save new item to Firebase under 'Bread Items'
            new_item_ref = ref.child('bread_items').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New bread item added successfully!")
            # Refresh the page after adding new item
            st.experimental_rerun()
        else:
            st.warning("Please enter both the bread item and price.")
