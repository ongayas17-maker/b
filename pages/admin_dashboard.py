import streamlit as st
from sqlalchemy import func
from database import User, Product, Order, CommunityPost, DiseaseDetection, OrderStatus, UserRole
from datetime import datetime, timedelta
import plotly.graph_objects as go

def show():
    if not st.session_state.user or st.session_state.user.role != UserRole.ADMIN:
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.markdown('<div class="main-header"><h1>🔧 Admin Dashboard</h1><p>System-wide overview and management</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_users}</h3><p>Active Users</p></div>', unsafe_allow_html=True)
    
    with col2:
        total_farmers = db.query(func.count(User.id)).filter(
            User.role == UserRole.FARMER, User.is_active == True
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_farmers}</h3><p>Farmers</p></div>', unsafe_allow_html=True)
    
    with col3:
        total_agrovets = db.query(func.count(User.id)).filter(
            User.role == UserRole.AGROVET, User.is_active == True
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_agrovets}</h3><p>Agrovets</p></div>', unsafe_allow_html=True)
    
    with col4:
        total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_products}</h3><p>Products</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_orders}</h3><p>Total Orders</p></div>', unsafe_allow_html=True)
    
    with col2:
        total_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.status == OrderStatus.COMPLETED
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>${total_revenue:.2f}</h3><p>Total Revenue</p></div>', unsafe_allow_html=True)
    
    with col3:
        total_posts = db.query(func.count(CommunityPost.id)).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_posts}</h3><p>Community Posts</p></div>', unsafe_allow_html=True)
    
    with col4:
        total_scans = db.query(func.count(DiseaseDetection.id)).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_scans}</h3><p>Disease Scans</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 User Growth (Last 30 Days)")
        
        days = []
        counts = []
        for i in range(29, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            count = db.query(func.count(User.id)).filter(
                User.created_at <= date
            ).scalar() or 0
            days.append(date.strftime('%m/%d'))
            counts.append(count)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=counts, mode='lines+markers', fill='tozeroy',
                                line=dict(color='#16a34a', width=2)))
        fig.update_layout(xaxis_title="Date", yaxis_title="Total Users", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Revenue Trend (Last 7 Days)")
        
        days = []
        revenue = []
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            day_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.status == OrderStatus.COMPLETED,
                func.date(Order.created_at) == date.date()
            ).scalar() or 0
            days.append(date.strftime('%a'))
            revenue.append(float(day_revenue))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=days, y=revenue, marker_color='#16a34a'))
        fig.update_layout(xaxis_title="Day", yaxis_title="Revenue ($)", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 Recent System Activity")
        
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        
        if recent_users:
            for user in recent_users:
                st.info(f"👤 New {user.role.value.title()}: **{user.full_name}** ({user.created_at.strftime('%Y-%m-%d')})")
        else:
            st.info("No recent activity")
    
    with col2:
        st.markdown("### ⚠️ System Alerts")
        
        pending_orders = db.query(func.count(Order.id)).filter(
            Order.status == OrderStatus.PENDING
        ).scalar() or 0
        
        if pending_orders > 0:
            st.warning(f"⚠️ {pending_orders} pending orders need attention")
        
        low_stock = db.query(func.count(Product.id)).filter(
            Product.stock_quantity < 10,
            Product.is_active == True
        ).scalar() or 0
        
        if low_stock > 0:
            st.warning(f"⚠️ {low_stock} products low on stock")
        
        if pending_orders == 0 and low_stock == 0:
            st.success("✅ All systems operational")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Admin Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.session_state.page = 'user_management'
            st.rerun()
    
    with col2:
        if st.button("📦 View All Orders", use_container_width=True):
            st.session_state.page = 'all_orders'
            st.rerun()
    
    with col3:
        if st.button("🏪 View All Products", use_container_width=True):
            st.session_state.page = 'all_products'
            st.rerun()
    
    with col4:
        if st.button("📊 System Analytics", use_container_width=True):
            st.session_state.page = 'system_analytics'
            st.rerun()
