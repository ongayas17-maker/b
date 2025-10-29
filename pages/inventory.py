import streamlit as st
from database import Product
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to manage inventory")
        return
    
    st.markdown('<div class="main-header"><h1>📊 Inventory Management</h1><p>Manage your product catalog and stock levels</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2 = st.tabs(["📦 All Products", "➕ Add New Product"])
    
    with tab1:
        show_products(db)
    
    with tab2:
        add_product(db)

def show_products(db):
    """Display all products"""
    
    st.markdown("### Product Catalog")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search = st.text_input("🔍 Search products", placeholder="Search by name or category...")
    
    with col2:
        show_inactive = st.checkbox("Show Inactive")
    
    query = db.query(Product).filter(Product.agrovet_id == st.session_state.user.id)
    
    if not show_inactive:
        query = query.filter(Product.is_active == True)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    products = query.all()
    
    if products:
        for product in products:
            with st.expander(f"{'✅' if product.is_active else '❌'} {product.name} - ${product.price:.2f} (Stock: {product.stock_quantity})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Product Name", value=product.name, key=f"name_{product.id}")
                    new_category = st.selectbox("Category", 
                        ["Pesticides", "Fertilizers", "Seeds", "Tools", "Medications"],
                        index=["Pesticides", "Fertilizers", "Seeds", "Tools", "Medications"].index(product.category) if product.category in ["Pesticides", "Fertilizers", "Seeds", "Tools", "Medications"] else 0,
                        key=f"cat_{product.id}")
                    new_description = st.text_area("Description", value=product.description or "", key=f"desc_{product.id}")
                
                with col2:
                    new_price = st.number_input("Price ($)", min_value=0.01, value=float(product.price), step=0.01, key=f"price_{product.id}")
                    new_stock = st.number_input("Stock Quantity", min_value=0, value=product.stock_quantity, key=f"stock_{product.id}")
                    new_manufacturer = st.text_input("Manufacturer", value=product.manufacturer or "", key=f"mfg_{product.id}")
                    new_active = st.checkbox("Active", value=product.is_active, key=f"active_{product.id}")
                
                col_update, col_delete = st.columns(2)
                
                with col_update:
                    if st.button("💾 Update", key=f"update_{product.id}", use_container_width=True):
                        product.name = new_name
                        product.category = new_category
                        product.description = new_description
                        product.price = new_price
                        product.stock_quantity = new_stock
                        product.manufacturer = new_manufacturer
                        product.is_active = new_active
                        db.commit()
                        st.success(f"Updated {product.name}!")
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️ Delete", key=f"delete_{product.id}", use_container_width=True):
                        db.delete(product)
                        db.commit()
                        st.success("Product deleted!")
                        st.rerun()
    else:
        st.info("No products found. Add your first product using the 'Add New Product' tab.")

def add_product(db):
    """Add new product form"""
    
    st.markdown("### Add New Product")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Product Name *", placeholder="e.g., Organic Fertilizer 5kg")
            category = st.selectbox("Category *", ["Pesticides", "Fertilizers", "Seeds", "Tools", "Medications"])
            description = st.text_area("Description", placeholder="Product details and usage instructions...")
        
        with col2:
            price = st.number_input("Price ($) *", min_value=0.01, value=10.00, step=0.01)
            stock_quantity = st.number_input("Initial Stock Quantity *", min_value=0, value=100)
            manufacturer = st.text_input("Manufacturer", placeholder="e.g., AgriTech Inc.")
        
        submit = st.form_submit_button("➕ Add Product", use_container_width=True)
        
        if submit:
            if not name or price <= 0:
                st.error("Please fill in all required fields (*)")
            else:
                product = Product(
                    name=name,
                    category=category,
                    description=description,
                    price=price,
                    stock_quantity=stock_quantity,
                    manufacturer=manufacturer,
                    agrovet_id=st.session_state.user.id,
                    created_at=datetime.utcnow(),
                    is_active=True
                )
                
                db.add(product)
                db.commit()
                
                st.success(f"✅ Product '{name}' added successfully!")
                st.balloons()
                
                if st.button("View Products"):
                    st.rerun()
