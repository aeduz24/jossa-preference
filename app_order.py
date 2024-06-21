import streamlit as st

# Define the original list of items
original_order = ["Item A", "Item B", "Item C", "Item D"]

st.title("Reorder Items")

# Display the original order
st.header("Original Order")
st.write(original_order)

# Allow the user to reorder the items using a multiselect
st.header("Reorder the Items new")

# Create a dictionary to track the current order
reordered_items = {item: idx for idx, item in enumerate(original_order)}

# Sort items by their original order
ordered_items = sorted(reordered_items, key=reordered_items.get)

# Create a multiselect with the original order as default
new_order = st.multiselect(
    "Drag to reorder:",
    ordered_items,
    default=ordered_items,
    format_func=lambda x: x
)

# Display the new order
st.header("New Order")
st.write(new_order)

# Optional: If needed, you can convert the order to indices or other formats for further processing
new_order_indices = [original_order.index(item) for item in new_order]
st.write("New Order Indices:", new_order_indices)

# Example use of the reordered list
# You can add code here to handle the reordered list as needed
