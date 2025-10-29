import streamlit as st
from sqlalchemy import func, desc
from database import Product, Order, OrderStatus, CustomerInteraction
from datetime import datetime, timedelta
import plotly.graph_objects as go

def show():
    if not st.session_state.user:
        st.warning("Please login to access the dashboard")
        return
    
    st.markdown('<div class="main-header"><h1>🏪 Agrovet Dashboard</h1><p>Your business command center</p></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    db = st.session_state.db
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = db.query(func.count(Product.id)).filter(
            Product.agrovet_id == user.id
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_products}</h3><p>Products</p></div>', unsafe_allow_html=True)
    
    with col2:
        total_orders = db.query(func.count(Order.id)).filter(
            Order.agrovet_id == user.id
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_orders}</h3><p>Total Orders</p></div>', unsafe_allow_html=True)
    
    with col3:
        pending_orders = db.query(func.count(Order.id)).filter(
            Order.agrovet_id == user.id,
            Order.status == OrderStatus.PENDING
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{pending_orders}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    
    with col4:
        total_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.agrovet_id == user.id,
            Order.status == OrderStatus.COMPLETED
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>${total_revenue:.2f}</h3><p>Total Revenue</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Recent Orders")
        
        recent_orders = db.query(Order).filter(
            Order.agrovet_id == user.id
        ).order_by(desc(Order.created_at)).limit(5).all()
        
        if recent_orders:
            for order in recent_orders:
                status_emoji = {
                    OrderStatus.PENDING: "🟡",
                    OrderStatus.PROCESSING: "🔵",
                    OrderStatus.COMPLETED: "🟢",
                    OrderStatus.CANCELLED: "🔴"
                }
                
                with st.expander(f"{status_emoji.get(order.status, '⚪')} Order #{order.id} - ${order.total_amount:.2f}"):
                    st.write(f"**Customer:** {order.farmer.full_name}")
                    st.write(f"**Status:** {order.status.value.title()}")
                    st.write(f"**Date:** {order.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Items:** {len(order.order_items)}")
        else:
            st.info("No orders yet")
    
    with col2:
        st.markdown("### 📊 Sales Trend (Last 7 Days)")
        
        days = []
        sales = []
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0)
            day_end = date.replace(hour=23, minute=59, second=59)
            
            daily_sales = db.query(func.sum(Order.total_amount)).filter(
                Order.agrovet_id == user.id,
                Order.created_at >= day_start,
                Order.created_at <= day_end,
                Order.status == OrderStatus.COMPLETED
            ).scalar() or 0
            
            days.append(date.strftime('%a'))
            sales.append(float(daily_sales))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=days, y=sales, marker_color='#16a34a'))
        fig.update_layout(
            title="Daily Sales",
            xaxis_title="Day",
            yaxis_title="Sales ($)",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📉 Low Stock Alert")
    
    low_stock_products = db.query(Product).filter(
        Product.agrovet_id == user.id,
        Product.stock_quantity < 10,
        Product.is_active == True
    ).all()
    
    if low_stock_products:
        for product in low_stock_products:
            st.warning(f"⚠️ **{product.name}** - Only {product.stock_quantity} units left!")
    else:
        st.success("✅ All products are well stocked")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 POS System", use_container_width=True):
            st.session_state.page = 'pos_system'
            st.rerun()
    
    with col2:
        if st.button("📦 Process Orders", use_container_width=True):
            st.session_state.page = 'agrovet_orders'
            st.rerun()
    
    with col3:
        if st.button("📊 Manage Inventory", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()
    
    with col4:
        if st.button("👥 CRM", use_container_width=True):
            st.session_state.page = 'crm'
            st.rerun()
