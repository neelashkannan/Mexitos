import streamlit as st
from firebase_data import fetch_Biryani_items

def display_Biryani_items_button(ref, session_state):
    Biryani_items = fetch_Biryani_items(ref)

    if Biryani_items:
        if st.button("Biryani :stew:", use_container_width=200):
            session_state['button_state_Biryani'] = not session_state['button_state_Biryani']

    if session_state['button_state_Biryani']:
        with st.container():
            for item_id, item_data in Biryani_items.items():
                if item_data.get('available', False):  # Check if the item is available
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.text(f"{item_data['item_name']} - {item_data['price']}")
                    with col2:
                        quantity = session_state['cart'].get(item_id, 0)
                        if quantity == 0:
                            if st.button(f"Add to Cart", key=f"add_Biryani_{item_id}"):
                                quantity += 1
                                session_state['cart'][item_id] = quantity
                                st.rerun()
                        else:
                            remove_button_key = f"remove_{item_id}"
                            if st.button("Remove from Cart", key=remove_button_key):
                                quantity -= 1
                                session_state['cart'][item_id] = quantity if quantity > 0 else 0
                                st.rerun()
