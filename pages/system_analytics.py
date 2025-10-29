import streamlit as st
from database import User, Product, Order, CommunityPost, DiseaseDetection, OrderStatus, UserRole
from sqlalchemy import func
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def show():
    if not st.session_state.user or st.session_state.user.role != UserRole.ADMIN:
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.markdown('<div class="main-header"><h1>📊 System Analytics</h1><p>Comprehensive platform insights</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 User Distribution by Role")
        
        role_counts = {}
        for role in UserRole:
            count = db.query(func.count(User.id)).filter(
                User.role == role,
                User.is_active == True
            ).scalar() or 0
            if count > 0:
                role_counts[role.value.title()] = count
        
        if role_counts:
            fig = go.Figure(data=[go.Pie(labels=list(role_counts.keys()), values=list(role_counts.values()),
                                         marker=dict(colors=['#16a34a', '#f97316', '#3b82f6']))])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No user data available")
    
    with col2:
        st.markdown("### 📦 Order Status Distribution")
        
        status_counts = {}
        for status in OrderStatus:
            count = db.query(func.count(Order.id)).filter(Order.status == status).scalar() or 0
            if count > 0:
                status_counts[status.value.title()] = count
        
        if status_counts:
            fig = go.Figure(data=[go.Pie(labels=list(status_counts.keys()), values=list(status_counts.values()))])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available")
    
    st.markdown("---")
    
    st.markdown("### 💰 Revenue Analysis (Last 30 Days)")
    
    daily_revenue = []
    dates = []
    
    for i in range(29, -1, -1):
        date = datetime.utcnow() - timedelta(days=i)
        revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.status == OrderStatus.COMPLETED,
            func.date(Order.created_at) == date.date()
        ).scalar() or 0
        
        dates.append(date.strftime('%m/%d'))
        daily_revenue.append(float(revenue))
    
    df = pd.DataFrame({'Date': dates, 'Revenue': daily_revenue})
    fig = px.area(df, x='Date', y='Revenue', title="Daily Revenue Trend")
    fig.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌱 Disease Detection Activity")
        
        detection_counts = []
        dates = []
        
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            count = db.query(func.count(DiseaseDetection.id)).filter(
                func.date(DiseaseDetection.created_at) == date.date()
            ).scalar() or 0
            
            dates.append(date.strftime('%a'))
            detection_counts.append(count)
        
        fig = go.Figure(data=[go.Bar(x=dates, y=detection_counts, marker_color='#16a34a')])
        fig.update_layout(xaxis_title="Day", yaxis_title="Scans", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💬 Community Engagement")
        
        posts_per_week = []
        weeks = []
        
        for i in range(3, -1, -1):
            week_start = datetime.utcnow() - timedelta(weeks=i)
            week_end = week_start + timedelta(days=7)
            
            count = db.query(func.count(CommunityPost.id)).filter(
                CommunityPost.created_at >= week_start,
                CommunityPost.created_at < week_end
            ).scalar() or 0
            
            weeks.append(f"Week {4-i}")
            posts_per_week.append(count)
        
        fig = go.Figure(data=[go.Bar(x=weeks, y=posts_per_week, marker_color='#3b82f6')])
        fig.update_layout(xaxis_title="Week", yaxis_title="Posts", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Platform Growth Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        today_users = db.query(func.count(User.id)).filter(
            func.date(User.created_at) == datetime.utcnow().date()
        ).scalar() or 0
        st.metric("New Users Today", today_users)
    
    with col2:
        today_orders = db.query(func.count(Order.id)).filter(
            func.date(Order.created_at) == datetime.utcnow().date()
        ).scalar() or 0
        st.metric("Orders Today", today_orders)
    
    with col3:
        today_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.status == OrderStatus.COMPLETED,
            func.date(Order.created_at) == datetime.utcnow().date()
        ).scalar() or 0
        st.metric("Revenue Today", f"${today_revenue:.2f}")
