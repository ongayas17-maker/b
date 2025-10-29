import streamlit as st
from database import Order, OrderStatus, Product, OrderItem
from sqlalchemy import func
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def show():
    if not st.session_state.user:
        st.warning("Please login to view analytics")
        return
    
    st.markdown('<div class="main-header"><h1>📈 Business Analytics</h1><p>Insights to grow your agrovet business</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.agrovet_id == st.session_state.user.id,
            Order.status == OrderStatus.COMPLETED
        ).scalar() or 0
        st.metric("Total Revenue", f"${total_revenue:.2f}")
    
    with col2:
        total_orders = db.query(func.count(Order.id)).filter(
            Order.agrovet_id == st.session_state.user.id
        ).scalar() or 0
        st.metric("Total Orders", total_orders)
    
    with col3:
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        st.metric("Average Order", f"${avg_order:.2f}")
    
    with col4:
        this_month_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.agrovet_id == st.session_state.user.id,
            Order.status == OrderStatus.COMPLETED,
            Order.created_at >= datetime.utcnow().replace(day=1)
        ).scalar() or 0
        st.metric("This Month", f"${this_month_revenue:.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Monthly Revenue Trend")
        
        monthly_data = []
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i*30)
            month_start = date.replace(day=1)
            
            revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.agrovet_id == st.session_state.user.id,
                Order.status == OrderStatus.COMPLETED,
                Order.created_at >= month_start
            ).scalar() or 0
            
            monthly_data.append({
                'month': month_start.strftime('%b %Y'),
                'revenue': float(revenue)
            })
        
        df = pd.DataFrame(monthly_data)
        fig = px.line(df, x='month', y='revenue', markers=True)
        fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📦 Top Selling Products")
        
        top_products = db.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem).filter(
            Product.agrovet_id == st.session_state.user.id
        ).group_by(Product.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
        
        if top_products:
            products = [p.name for p in top_products]
            quantities = [p.total_sold for p in top_products]
            
            fig = go.Figure(data=[go.Bar(x=products, y=quantities, marker_color='#16a34a')])
            fig.update_layout(xaxis_title="Product", yaxis_title="Units Sold", height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data available yet")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Order Status Distribution")
        
        status_counts = {}
        for status in OrderStatus:
            count = db.query(func.count(Order.id)).filter(
                Order.agrovet_id == st.session_state.user.id,
                Order.status == status
            ).scalar() or 0
            if count > 0:
                status_counts[status.value.title()] = count
        
        if status_counts:
            fig = go.Figure(data=[go.Pie(labels=list(status_counts.keys()), values=list(status_counts.values()))])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available")
    
    with col2:
        st.markdown("### 💰 Revenue by Category")
        
        category_revenue = db.query(
            Product.category,
            func.sum(OrderItem.subtotal).label('revenue')
        ).join(OrderItem).join(Order).filter(
            Product.agrovet_id == st.session_state.user.id,
            Order.status == OrderStatus.COMPLETED
        ).group_by(Product.category).all()
        
        if category_revenue:
            categories = [c.category or 'Uncategorized' for c in category_revenue]
            revenues = [float(c.revenue) for c in category_revenue]
            
            fig = go.Figure(data=[go.Pie(labels=categories, values=revenues)])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
