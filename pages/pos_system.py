import streamlit as st
from database import Product, Order, OrderItem, OrderStatus, User, UserRole
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to access the POS system")
        return
    
    st.markdown('<div class="main-header"><h1>💰 Point of Sale System</h1><p>Process customer purchases quickly and efficiently</p></div>', unsafe_allow_html=True)
    
    if 'pos_cart' not in st.session_state:
        st.session_state.pos_cart = []
    
    if 'selected_customer' not in st.session_state:
        st.session_state.selected_customer = None
    
    db = st.session_state.db
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 Product Search")
        
        search = st.text_input("Search products", placeholder="Type product name or scan barcode...")
        
        if search:
            products = db.query(Product).filter(
                Product.agrovet_id == st.session_state.user.id,
                Product.is_active == True,
                Product.stock_quantity > 0,
                Product.name.ilike(f"%{search}%")
            ).limit(10).all()
            
            if products:
                for product in products:
                    col_name, col_price, col_stock, col_add = st.columns([3, 1, 1, 1])
                    
                    with col_name:
                        st.write(f"**{product.name}**")
                    with col_price:
                        st.write(f"${product.price:.2f}")
                    with col_stock:
                        st.write(f"Stock: {product.stock_quantity}")
                    with col_add:
                        if st.button("➕", key=f"add_pos_{product.id}"):
                            add_to_pos_cart(product)
            else:
                st.info("No products found")
        
        st.markdown("---")
        
        st.markdown("### 🛒 Current Sale")
        
        if st.session_state.pos_cart:
            for idx, item in enumerate(st.session_state.pos_cart):
                col_name, col_qty, col_price, col_total, col_remove = st.columns([3, 1, 1, 1, 1])
                
                with col_name:
                    st.write(item['name'])
                with col_qty:
                    new_qty = st.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{idx}", label_visibility="collapsed")
                    if new_qty != item['quantity']:
                        st.session_state.pos_cart[idx]['quantity'] = new_qty
                        st.rerun()
                with col_price:
                    st.write(f"${item['price']:.2f}")
                with col_total:
                    st.write(f"${item['price'] * item['quantity']:.2f}")
                with col_remove:
                    if st.button("🗑️", key=f"remove_pos_{idx}"):
                        st.session_state.pos_cart.pop(idx)
                        st.rerun()
        else:
            st.info("Cart is empty. Search and add products to start a sale.")
    
    with col2:
        st.markdown("### 💵 Payment")
        
        if st.session_state.pos_cart:
            subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.pos_cart)
            tax_rate = 0.0
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0 0 1rem 0;'>Order Summary</h3>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span>Subtotal:</span><span>${subtotal:.2f}</span>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span>Tax ({tax_rate*100}%):</span><span>${tax:.2f}</span>
                </div>
                <hr>
                <div style='display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: bold; color: #16a34a;'>
                    <span>Total:</span><span>${total:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("#### Customer Information")
            
            farmers = db.query(User).filter(User.role == UserRole.FARMER, User.is_active == True).all()
            customer_options = ["Walk-in Customer"] + [f"{f.full_name} ({f.username})" for f in farmers]
            
            selected_customer = st.selectbox("Select Customer", customer_options)
            
            if selected_customer != "Walk-in Customer":
                customer_id = farmers[customer_options.index(selected_customer) - 1].id
            else:
                customer_id = None
            
            payment_method = st.selectbox("Payment Method", ["Cash", "Mobile Money", "Card", "Credit"])
            
            notes = st.text_area("Order Notes", placeholder="Any special notes for this order...")
            
            st.markdown("---")
            
            col_cancel, col_complete = st.columns(2)
            
            with col_cancel:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.pos_cart = []
                    st.rerun()
            
            with col_complete:
                if st.button("✅ Complete Sale", type="primary", use_container_width=True):
                    complete_sale(customer_id, total, payment_method, notes)
        else:
            st.info("Add products to cart to proceed with checkout")
            
            st.markdown("---")
            st.markdown("### 🔢 Quick Keypad")
            st.markdown("Scan barcode or use quick add buttons")

def add_to_pos_cart(product):
    """Add product to POS cart"""
    for item in st.session_state.pos_cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            st.success(f"Updated {product.name}")
            st.rerun()
            return
    
    st.session_state.pos_cart.append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': 1
    })
    st.success(f"Added {product.name}")
    st.rerun()

def complete_sale(customer_id, total, payment_method, notes):
    """Complete the POS sale"""
    try:
        db = st.session_state.db
        
        order = Order(
            farmer_id=customer_id,
            agrovet_id=st.session_state.user.id,
            total_amount=total,
            status=OrderStatus.COMPLETED,
            delivery_address="In-store purchase",
            notes=f"Payment: {payment_method}. {notes}",
            created_at=datetime.utcnow()
        )
        
        db.add(order)
        db.flush()
        
        for item in st.session_state.pos_cart:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['id'],
                quantity=item['quantity'],
                unit_price=item['price'],
                subtotal=item['quantity'] * item['price']
            )
            db.add(order_item)
            
            product = db.query(Product).filter(Product.id == item['id']).first()
            if product:
                product.stock_quantity -= item['quantity']
        
        db.commit()
        
        st.session_state.pos_cart = []
        st.success(f"✅ Sale completed! Order #{order.id} - Total: ${total:.2f}")
        st.balloons()
        
        st.markdown("---")
        st.markdown(f"""
        <div style='background: #dcfce7; padding: 2rem; border-radius: 10px; text-align: center;'>
            <h2>Receipt</h2>
            <p>Order #: {order.id}</p>
            <p>Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}</p>
            <h3>Total: ${total:.2f}</h3>
            <p>Payment Method: {payment_method}</p>
            <p>Thank you for your purchase!</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        db.rollback()
        st.error(f"Error completing sale: {str(e)}")
