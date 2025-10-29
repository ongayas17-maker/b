import streamlit as st
from database import Product, Order, OrderItem, OrderStatus
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to access the marketplace")
        return
    
    st.markdown('<div class="main-header"><h1>🛒 Agricultural Marketplace</h1><p>Browse and order products from verified agrovets</p></div>', unsafe_allow_html=True)
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search = st.text_input("🔍 Search products", placeholder="Search by name, category, or manufacturer...")
    
    with col2:
        category_filter = st.selectbox("Category", ["All", "Pesticides", "Fertilizers", "Seeds", "Tools", "Medications"])
    
    st.markdown("---")
    
    col_products, col_cart = st.columns([2, 1])
    
    with col_products:
        st.markdown("### 📦 Available Products")
        
        db = st.session_state.db
        query = db.query(Product).filter(Product.is_active == True, Product.stock_quantity > 0)
        
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        
        if category_filter != "All":
            query = query.filter(Product.category == category_filter)
        
        products = query.all()
        
        if products:
            for product in products:
                with st.container():
                    col_img, col_info, col_action = st.columns([1, 3, 1])
                    
                    with col_img:
                        if product.image_url:
                            st.image(product.image_url, use_container_width=True)
                        else:
                            st.image(f"https://via.placeholder.com/150?text={product.name[:10]}", use_container_width=True)
                    
                    with col_info:
                        st.markdown(f"### {product.name}")
                        st.write(f"**Category:** {product.category or 'General'}")
                        st.write(f"**Price:** ${product.price:.2f}")
                        st.write(f"**In Stock:** {product.stock_quantity} units")
                        if product.description:
                            st.caption(product.description[:100] + "..." if len(product.description) > 100 else product.description)
                    
                    with col_action:
                        st.markdown("<br>", unsafe_allow_html=True)
                        quantity = st.number_input(f"Qty", min_value=1, max_value=product.stock_quantity, value=1, key=f"qty_{product.id}")
                        if st.button("🛒 Add", key=f"add_{product.id}", use_container_width=True):
                            add_to_cart(product, quantity)
                    
                    st.markdown("---")
        else:
            st.info("No products found matching your criteria")
    
    with col_cart:
        st.markdown("### 🛍️ Shopping Cart")
        
        if st.session_state.cart:
            total = 0
            for idx, item in enumerate(st.session_state.cart):
                with st.container():
                    st.write(f"**{item['name']}**")
                    st.write(f"Qty: {item['quantity']} × ${item['price']:.2f}")
                    st.write(f"**${item['quantity'] * item['price']:.2f}**")
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                    st.markdown("---")
                total += item['quantity'] * item['price']
            
            st.markdown(f"### Total: **${total:.2f}**")
            
            delivery_address = st.text_area("Delivery Address", placeholder="Enter your delivery address...")
            notes = st.text_area("Order Notes (Optional)", placeholder="Any special instructions?")
            
            if st.button("✅ Place Order", type="primary", use_container_width=True):
                if not delivery_address:
                    st.error("Please enter a delivery address")
                else:
                    place_order(delivery_address, notes, total)
        else:
            st.info("Your cart is empty. Add products to get started!")
            st.image("https://via.placeholder.com/200?text=Empty+Cart", use_container_width=True)

def add_to_cart(product, quantity):
    """Add product to cart"""
    for item in st.session_state.cart:
        if item['id'] == product.id:
            item['quantity'] += quantity
            st.success(f"Updated {product.name} quantity in cart!")
            return
    
    st.session_state.cart.append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': quantity
    })
    st.success(f"Added {product.name} to cart!")

def place_order(delivery_address, notes, total):
    """Create order from cart"""
    try:
        db = st.session_state.db
        
        order = Order(
            farmer_id=st.session_state.user.id,
            total_amount=total,
            status=OrderStatus.PENDING,
            delivery_address=delivery_address,
            notes=notes,
            created_at=datetime.utcnow()
        )
        
        db.add(order)
        db.flush()
        
        for item in st.session_state.cart:
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
        
        st.session_state.cart = []
        st.success(f"✅ Order #{order.id} placed successfully! Total: ${total:.2f}")
        st.balloons()
        
        if st.button("View My Orders"):
            st.session_state.page = 'my_orders'
            st.rerun()
        
    except Exception as e:
        db.rollback()
        st.error(f"Error placing order: {str(e)}")
