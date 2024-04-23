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

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
page = st.sidebar.selectbox("Choose a page", ["Orders", "Chicken Dry","Bread Items","Shawarma", "rice/noodles/kothu", "Starters", "Biryani"])
def on_order_added(order_snapshot):
    order_data = order_snapshot.val()
    st.write(f"New order added: {order_data}")
    st.experimental_rerun()



if page == "Orders":
    st.markdown("# Orders")
    orders_data = ref.child('orders').get()
    if orders_data:
        orders_ref = ref.child('orders')
        orders_ref.listen(on_order_added)
        for order_number, order_data in orders_data.items():
            st.markdown(f"## Order {order_number}")
            cart = order_data.get('cart')
            total = order_data.get('total')
            name = order_data.get('name')
            phone_number = order_data.get('phone_number')
            order_date = order_data.get('order_date')
            if cart is not None and total is not None and name is not None and phone_number is not None:
                items_table = "| Item | Quantity | Price | Total |\n|---|---|---|---|\n"
                order_total = 0
                for item_data in cart:
                    item_name = item_data.get('item_name', 'N/A')
                    item_quantity = item_data.get('quantity', 0)
                    item_price = item_data.get('price', 0)
                    item_total = item_quantity * item_price
                    items_table += f"| {item_name} | {item_quantity} | {item_price} | {item_total} |\n"
                    order_total += item_total
                items_table += f"| **Total Order Amount:** | | | {order_total} |\n"
                st.markdown(items_table, unsafe_allow_html=True)
                st.write(f"**Customer Name:** {name}")
                st.write(f"**Phone Number:** {phone_number}")
                st.write(f"**Order Date:** {order_date}")
                if st.button(f"Mark Order {order_number} as Delivered"):
                    delivered_orders_ref = ref.child('delivered_orders')
                    delivered_orders_ref.push(order_data)
                    ref.child('orders').child(order_number).delete()
                    st.success(f"Order {order_number} marked as delivered and removed from current orders!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning(f"Order {order_number} data is incomplete or unavailable.")
    
    if st.checkbox('Start Auto-Refresh'):
        st.write('Auto-refresh is on. Orders page will be refreshed every 10 seconds.')
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 10:
                st.rerun()
                start_time = time.time()
            time.sleep(1)

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

elif page == "Shawarma":
    st.markdown("## Shawarma Menu")

    existing_items = ref.child('shawarma').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"shawarma_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('shawarma').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.experimental_rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('shawarma').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.experimental_rerun()

    # Add new item form for Shawarma
    st.markdown("### Add New Shawarma Item")
    new_item = st.text_input("Enter Shawarma Item")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add Shawarma Item"):
        if new_item and price:
            # Save new item to Firebase under 'Shawarma'
            new_item_ref = ref.child('shawarma').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New Shawarma item added successfully!")
            # Refresh the page after adding new item
            st.experimental_rerun()
        else:
            st.warning("Please enter both the Shawarma item and price.")

elif page == "rice/noodles/kothu":
    st.markdown("## rice/noodles/kothu")

    existing_items = ref.child('rice and noodles items').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"shawarma_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('rice and noodles items').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.experimental_rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('rice and noodles items').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.experimental_rerun()

    # Add new item form for Shawarma
    st.markdown("### Add New rice and noodles items")
    new_item = st.text_input("Enter rice and noodles items")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add rice and noodles items"):
        if new_item and price:
            # Save new item to Firebase under 'Shawarma'
            new_item_ref = ref.child('rice and noodles items').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New rice and noodles item added successfully!")
            # Refresh the page after adding new item
            st.experimental_rerun()
        else:
            st.warning("Please enter both the rice and noodles items and price.")

elif page == "Starters":
    st.markdown("## starters")

    existing_items = ref.child('starters').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"shawarma_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Add new item form for Shawarma
    st.markdown("### starter items")
    new_item = st.text_input("Enter starter items")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add starter items"):
        if new_item and price:
            # Save new item to Firebase under 'Shawarma'
            new_item_ref = ref.child('starters').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New starter item added successfully!")
            # Refresh the page after adding new item
            st.rerun()
        else:
            st.warning("Please enter both the starter items and price.")

elif page == "Biryani":
    st.markdown("## Biryani")

    existing_items = ref.child('Biryani').get()
    if existing_items:
        for item_key, item_data in existing_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} - {item_data['price']} Rupees")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"shawarma_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Biryani').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Biryani').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Add new item form for Shawarma
    st.markdown("### Biryani items")
    new_item = st.text_input("Enter Biryani items")
    price = st.number_input("Enter Price (Rupees)", min_value=0)

    if st.button("Add Biryani items"):
        if new_item and price:
            # Save new item to Firebase under 'Shawarma'
            new_item_ref = ref.child('Biryani').push()
            new_item_ref.set({
                'item_name': new_item,
                'price': price,
                'available': True  # Default status is available
            })
            st.success("New starter item added successfully!")
            # Refresh the page after adding new item
            st.rerun()
        else:
            st.warning("Please enter both the starter items and price.")
