import streamlit as st
from database import Product

def show():
    if not st.session_state.user or st.session_state.user.role.value != 'admin':
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.markdown('<div class="main-header"><h1>🏪 All Products</h1><p>System-wide product catalog</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search = st.text_input("🔍 Search products", placeholder="Search by name, category, or manufacturer...")
    
    with col2:
        show_inactive = st.checkbox("Show Inactive")
    
    query = db.query(Product)
    
    if not show_inactive:
        query = query.filter(Product.is_active == True)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.category.ilike(f"%{search}%")) |
            (Product.manufacturer.ilike(f"%{search}%"))
        )
    
    products = query.all()
    
    if products:
        for product in products:
            agrovet_name = product.agrovet_id
            agrovet = db.query(User).filter(User.id == agrovet_name).first() if agrovet_name else None
            
            status_icon = "✅" if product.is_active else "❌"
            
            with st.expander(f"{status_icon} {product.name} - ${product.price:.2f} (Stock: {product.stock_quantity})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Product Name:** {product.name}")
                    st.write(f"**Category:** {product.category or 'N/A'}")
                    st.write(f"**Price:** ${product.price:.2f}")
                    st.write(f"**Stock:** {product.stock_quantity} units")
                
                with col2:
                    st.write(f"**Manufacturer:** {product.manufacturer or 'N/A'}")
                    st.write(f"**Agrovet:** {agrovet.full_name if agrovet else 'Unknown'}")
                    st.write(f"**Status:** {'Active' if product.is_active else 'Inactive'}")
                    st.write(f"**Added:** {product.created_at.strftime('%Y-%m-%d')}")
                
                if product.description:
                    st.write(f"**Description:** {product.description}")
    else:
        st.info("No products found")

from database import User
