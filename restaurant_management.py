import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Page configuration
st.set_page_config(
    page_title="Smart Restaurant Billing System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff6a00 0%, #ee0979 50%, #6a00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .bill-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .order-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #ff6a00;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .payment-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .menu-item {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .menu-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(254,107,139,0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(254,107,139,0.6);
    }
    
    .discount-badge {
        background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .notification {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #ff6a00;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced menu items with categories, descriptions, and special offers
menu_items = {
    "🥗 Starters": {
        "Finger Chips": {"price": 80, "description": "Crispy golden fries", "category": "veg", "spicy": False},
        "Paneer Chilly": {"price": 170, "description": "Spicy paneer in Chinese style", "category": "veg", "spicy": True},
        "Manchurian": {"price": 120, "description": "Vegetable balls in tangy sauce", "category": "veg", "spicy": True},
        "Chicken Wings": {"price": 200, "description": "Spicy grilled chicken wings", "category": "non-veg", "spicy": True},
        "Fish Tikka": {"price": 250, "description": "Tandoori fish pieces", "category": "non-veg", "spicy": True}
    },
    "🍲 Soups": {
        "Tomato Soup": {"price": 90, "description": "Fresh tomato soup", "category": "veg", "spicy": False},
        "Manchow Soup": {"price": 120, "description": "Spicy Chinese soup", "category": "veg", "spicy": True},
        "Sweet Corn Soup": {"price": 110, "description": "Creamy sweet corn", "category": "veg", "spicy": False},
        "Chicken Soup": {"price": 140, "description": "Hot chicken broth", "category": "non-veg", "spicy": False}
    },
    "🥘 Main Course": {
        "Paneer Bhurji": {"price": 180, "description": "Scrambled paneer curry", "category": "veg", "spicy": True},
        "Kaju Curry": {"price": 220, "description": "Rich cashew curry", "category": "veg", "spicy": False},
        "Veg Handi": {"price": 150, "description": "Mixed vegetable curry", "category": "veg", "spicy": True},
        "Butter Chicken": {"price": 280, "description": "Creamy chicken curry", "category": "non-veg", "spicy": False},
        "Mutton Curry": {"price": 320, "description": "Spicy mutton curry", "category": "non-veg", "spicy": True}
    },
    "🫓 Breads": {
        "Phulka Roti": {"price": 8, "description": "Soft wheat bread", "category": "veg", "spicy": False},
        "Butter Naan": {"price": 40, "description": "Buttery naan bread", "category": "veg", "spicy": False},
        "Paneer Kulcha": {"price": 40, "description": "Stuffed paneer bread", "category": "veg", "spicy": False},
        "Garlic Naan": {"price": 45, "description": "Garlic flavored naan", "category": "veg", "spicy": False}
    },
    "🍰 Desserts": {
        "Gulab Jamun": {"price": 60, "description": "Sweet milk balls", "category": "veg", "spicy": False},
        "Ice Cream": {"price": 80, "description": "Vanilla ice cream", "category": "veg", "spicy": False},
        "Rasgulla": {"price": 70, "description": "Spongy cheese balls", "category": "veg", "spicy": False}
    },
    "🥤 Beverages": {
        "Lassi": {"price": 50, "description": "Yogurt drink", "category": "veg", "spicy": False},
        "Fresh Lime": {"price": 40, "description": "Fresh lime water", "category": "veg", "spicy": False},
        "Masala Tea": {"price": 20, "description": "Spiced tea", "category": "veg", "spicy": False},
        "Coffee": {"price": 30, "description": "Hot coffee", "category": "veg", "spicy": False}
    }
}

# Initialize session states
if "orders" not in st.session_state:
    st.session_state.orders = []
if "payment_mode" not in st.session_state:
    st.session_state.payment_mode = None
if "customer_info" not in st.session_state:
    st.session_state.customer_info = {}
if "daily_sales" not in st.session_state:
    st.session_state.daily_sales = []
if "discounts" not in st.session_state:
    st.session_state.discounts = {"percentage": 0, "fixed": 0}
if "table_number" not in st.session_state:
    st.session_state.table_number = 1

# Header
st.markdown('<div class="main-header">🍽️ Smart Restaurant Billing System</div>', unsafe_allow_html=True)

# Sidebar - Enhanced Order section
st.sidebar.header("📋 Place Your Order")

# Customer info section
with st.sidebar.expander("👤 Customer Information"):
    customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
    table_number = st.number_input("Table Number", min_value=1, max_value=50, value=1)
    phone_number = st.text_input("Phone Number", placeholder="Contact number")
    st.session_state.customer_info = {
        "name": customer_name,
        "table": table_number,
        "phone": phone_number
    }

# Menu selection with enhanced UI
st.sidebar.subheader("🍽️ Menu Selection")

# Category filter
category = st.sidebar.selectbox("Select Category", list(menu_items.keys()))

# Filter options
col1, col2 = st.sidebar.columns(2)
with col1:
    veg_filter = st.checkbox("🥬 Veg Only", value=False)
with col2:
    spicy_filter = st.checkbox("🌶️ Spicy Only", value=False)

# Filter items based on selection
filtered_items = {}
for item_name, item_data in menu_items[category].items():
    if veg_filter and item_data["category"] != "veg":
        continue
    if spicy_filter and not item_data["spicy"]:
        continue
    filtered_items[item_name] = item_data

if filtered_items:
    item = st.sidebar.selectbox("Select Item", list(filtered_items.keys()))
    
    # Display item details
    item_data = filtered_items[item]
    st.sidebar.markdown(f"""
    <div class="menu-item">
        <strong>{item}</strong><br>
        💰 ₹{item_data['price']}<br>
        📝 {item_data['description']}<br>
        {'🥬' if item_data['category'] == 'veg' else '🍖'} {'🌶️' if item_data['spicy'] else ''}
    </div>
    """, unsafe_allow_html=True)
    
    price = item_data['price']
    quantity = st.sidebar.number_input("Quantity", min_value=1, max_value=20, value=1)
    
    # Special instructions
    special_instructions = st.sidebar.text_area("Special Instructions", placeholder="e.g., Less spicy, Extra sauce")
    
    if st.sidebar.button("Add to Order ➕", key="add_order"):
        st.session_state.orders.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "category": category,
            "item": item,
            "price": price,
            "quantity": quantity,
            "total": price * quantity,
            "instructions": special_instructions,
            "item_type": item_data["category"],
            "spicy": item_data["spicy"]
        })
        st.sidebar.success(f"✅ Added {quantity} x {item}")
        st.rerun()
else:
    st.sidebar.info("No items match your filter criteria")

# Quick add popular items
st.sidebar.subheader("⚡ Quick Add Popular Items")
popular_items = [
    ("Butter Chicken", "🥘 Main Course", 280),
    ("Butter Naan", "🫓 Breads", 40),
    ("Masala Tea", "🥤 Beverages", 20)
]

for item, cat, price in popular_items:
    if st.sidebar.button(f"{item} - ₹{price}", key=f"quick_{item}"):
        st.session_state.orders.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "category": cat,
            "item": item,
            "price": price,
            "quantity": 1,
            "total": price,
            "instructions": "",
            "item_type": "veg" if item != "Butter Chicken" else "non-veg",
            "spicy": False
        })
        st.sidebar.success(f"✅ Added {item}")
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🧾 Order Summary")
    
    if st.session_state.orders:
        # Create enhanced dataframe
        df = pd.DataFrame(st.session_state.orders)
        
        # Add row numbers
        df.index = range(1, len(df) + 1)
        
        # Display order table with better formatting
        display_df = df[['timestamp', 'category', 'item', 'quantity', 'price', 'total', 'instructions']]
        display_df.columns = ['Time', 'Category', 'Item', 'Qty', 'Price (₹)', 'Total (₹)', 'Instructions']
        
        st.dataframe(display_df, use_container_width=True)
        
        # Order statistics
        total_items = df['quantity'].sum()
        total_bill = df['total'].sum()
        avg_item_price = df['price'].mean()
        
        # Calculate discounts
        discount_amount = 0
        if st.session_state.discounts["percentage"] > 0:
            discount_amount += total_bill * (st.session_state.discounts["percentage"] / 100)
        if st.session_state.discounts["fixed"] > 0:
            discount_amount += st.session_state.discounts["fixed"]
        
        # Calculate taxes
        tax_rate = 0.18  # 18% GST
        tax_amount = (total_bill - discount_amount) * tax_rate
        final_total = total_bill - discount_amount + tax_amount
        
        # Display bill details
        st.markdown(f"""
        <div class="bill-card">
            <h2>💰 Bill Summary</h2>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <span>Subtotal ({total_items} items):</span>
                <span>₹{total_bill:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <span>Discount:</span>
                <span>-₹{discount_amount:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <span>Tax (18% GST):</span>
                <span>₹{tax_amount:.2f}</span>
            </div>
            <hr style="border: 1px solid white; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: bold;">
                <span>Final Total:</span>
                <span>₹{final_total:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1_btn, col2_btn, col3_btn = st.columns(3)
        
        with col1_btn:
            if st.button("🗑️ Clear Last Item"):
                if st.session_state.orders:
                    st.session_state.orders.pop()
                    st.rerun()
        
        with col2_btn:
            if st.button("🔄 Clear All Orders"):
                st.session_state.orders = []
                st.rerun()
        
        with col3_btn:
            if st.button("📊 View Analytics"):
                st.session_state.show_analytics = True
    else:
        st.markdown("""
        <div class="notification">
            <h3>👋 Welcome to Smart Restaurant!</h3>
            <p>No items in your order yet. Please select items from the sidebar to get started.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("📈 Quick Stats")
    
    if st.session_state.orders:
        df = pd.DataFrame(st.session_state.orders)
        
        # Statistics cards
        total_items = df['quantity'].sum()
        total_value = df['total'].sum()
        avg_price = df['price'].mean()
        
        st.markdown(f"""
        <div class="stats-card">
            <h3>{total_items}</h3>
            <p>Total Items</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stats-card">
            <h3>₹{total_value:.0f}</h3>
            <p>Order Value</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stats-card">
            <h3>₹{avg_price:.0f}</h3>
            <p>Avg Item Price</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Order composition chart
        category_counts = df.groupby('category')['quantity'].sum().reset_index()
        if not category_counts.empty:
            fig = px.pie(category_counts, values='quantity', names='category',
                        title='Order Composition',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 Stats will appear once you add items to your order")

# Payment and Discount Section
if st.session_state.orders:
    st.subheader("💳 Payment & Discounts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="payment-card"><h3>💳 Payment Options</h3></div>', unsafe_allow_html=True)
        
        payment_methods = ["💵 Cash", "💳 Card", "📱 UPI", "💰 Digital Wallet"]
        st.session_state.payment_mode = st.selectbox("Choose Payment Method", payment_methods)
        
        # Special notes
        customer_note = st.text_area("📝 Special Notes", 
                                   placeholder="Any special instructions or notes for the order")
    
    with col2:
        st.markdown('<div class="payment-card"><h3>🏷️ Discounts</h3></div>', unsafe_allow_html=True)
        
        discount_type = st.selectbox("Discount Type", ["None", "Percentage", "Fixed Amount"])
        
        if discount_type == "Percentage":
            discount_value = st.slider("Discount Percentage", 0, 50, 0)
            st.session_state.discounts = {"percentage": discount_value, "fixed": 0}
        elif discount_type == "Fixed Amount":
            discount_value = st.number_input("Discount Amount (₹)", min_value=0, value=0)
            st.session_state.discounts = {"percentage": 0, "fixed": discount_value}
        else:
            st.session_state.discounts = {"percentage": 0, "fixed": 0}
        
        # Loyalty program
        is_member = st.checkbox("🏆 Loyalty Member")
        if is_member:
            st.success("5% loyalty discount applied!")
            st.session_state.discounts["percentage"] += 5

# Final Actions
if st.session_state.orders:
    st.subheader("✅ Final Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Generate bill
        if st.button("🧾 Generate Bill", type="primary"):
            # Add to daily sales
            bill_data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "customer": st.session_state.customer_info,
                "orders": st.session_state.orders,
                "payment_mode": st.session_state.payment_mode,
                "total_amount": sum(order['total'] for order in st.session_state.orders),
                "discount": st.session_state.discounts,
                "notes": customer_note
            }
            st.session_state.daily_sales.append(bill_data)
            
            st.success("✅ Bill generated successfully!")
            st.balloons()
    
    with col2:
        # Download detailed bill
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            
            # Create detailed bill
            detailed_bill = f"""
            SMART RESTAURANT BILLING SYSTEM
            ================================
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Customer: {st.session_state.customer_info.get('name', 'Walk-in')}
            Table: {st.session_state.customer_info.get('table', 'N/A')}
            Phone: {st.session_state.customer_info.get('phone', 'N/A')}
            
            ORDER DETAILS:
            ==============
            """
            
            for order in st.session_state.orders:
                detailed_bill += f"{order['item']} x {order['quantity']} = ₹{order['total']}\n"
            
            detailed_bill += f"""
            
            BILL SUMMARY:
            =============
            Subtotal: ₹{sum(order['total'] for order in st.session_state.orders):.2f}
            Discount: ₹{st.session_state.discounts['percentage'] + st.session_state.discounts['fixed']:.2f}
            Tax (18%): ₹{(sum(order['total'] for order in st.session_state.orders) * 0.18):.2f}
            
            Payment Mode: {st.session_state.payment_mode}
            
            Thank you for dining with us!
            """
            
            st.download_button(
                label="💾 Download Bill",
                data=detailed_bill,
                file_name=f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        # Print order (simulation)
        if st.button("🖨️ Print Order"):
            st.info("📄 Order sent to kitchen printer!")

# Analytics Dashboard
if st.session_state.daily_sales:
    st.subheader("📊 Analytics Dashboard")
    
    # Create analytics from daily sales
    sales_df = pd.DataFrame(st.session_state.daily_sales)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily sales chart
        daily_totals = sales_df.groupby('date')['total_amount'].sum().reset_index()
        fig = px.bar(daily_totals, x='date', y='total_amount',
                    title='Daily Sales Revenue',
                    labels={'total_amount': 'Revenue (₹)', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Payment mode distribution
        payment_counts = sales_df['payment_mode'].value_counts().reset_index()
        fig = px.pie(payment_counts, values='count', names='payment_mode',
                    title='Payment Mode Distribution')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 2rem;'>
    <h3>🍽️ Smart Restaurant Management</h3>
    <p>Streamlining your restaurant operations with modern technology</p>
    <p>Made with ❤️ for restaurant efficiency</p>
</div>
""", unsafe_allow_html=True)