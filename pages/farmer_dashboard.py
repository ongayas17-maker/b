import streamlit as st
from sqlalchemy import func, desc
from database import DiseaseDetection, Order, OrderStatus
from datetime import datetime, timedelta
import plotly.graph_objects as go

def show():
    if not st.session_state.user:
        st.warning("Please login to access the dashboard")
        return
    
    st.markdown('<div class="main-header"><h1>🏠 Farmer Dashboard</h1><p>Welcome to your agricultural command center</p></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    db = st.session_state.db
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_scans = db.query(func.count(DiseaseDetection.id)).filter(
            DiseaseDetection.user_id == user.id
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_scans}</h3><p>Disease Scans</p></div>', unsafe_allow_html=True)
    
    with col2:
        total_orders = db.query(func.count(Order.id)).filter(
            Order.farmer_id == user.id
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{total_orders}</h3><p>Total Orders</p></div>', unsafe_allow_html=True)
    
    with col3:
        pending_orders = db.query(func.count(Order.id)).filter(
            Order.farmer_id == user.id,
            Order.status == OrderStatus.PENDING
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{pending_orders}</h3><p>Pending Orders</p></div>', unsafe_allow_html=True)
    
    with col4:
        recent_diseases = db.query(func.count(DiseaseDetection.id)).filter(
            DiseaseDetection.user_id == user.id,
            DiseaseDetection.created_at >= datetime.utcnow() - timedelta(days=7)
        ).scalar() or 0
        st.markdown(f'<div class="stat-card"><h3>{recent_diseases}</h3><p>This Week</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔬 Recent Disease Detections")
        
        recent_detections = db.query(DiseaseDetection).filter(
            DiseaseDetection.user_id == user.id
        ).order_by(desc(DiseaseDetection.created_at)).limit(5).all()
        
        if recent_detections:
            for detection in recent_detections:
                with st.expander(f"🌿 {detection.disease_name or 'Unknown'} - {detection.created_at.strftime('%Y-%m-%d')}"):
                    st.write(f"**Plant:** {detection.plant_type or 'Not specified'}")
                    st.write(f"**Confidence:** {(detection.confidence_score or 0) * 100:.1f}%")
                    st.write(f"**Severity:** {detection.severity or 'Unknown'}")
                    if detection.treatment:
                        st.write(f"**Treatment:** {detection.treatment[:100]}...")
        else:
            st.info("No disease detections yet. Use the Disease Detection feature to scan your plants!")
    
    with col2:
        st.markdown("### 📦 Recent Orders")
        
        recent_orders = db.query(Order).filter(
            Order.farmer_id == user.id
        ).order_by(desc(Order.created_at)).limit(5).all()
        
        if recent_orders:
            for order in recent_orders:
                status_color = {
                    OrderStatus.PENDING: "🟡",
                    OrderStatus.PROCESSING: "🔵",
                    OrderStatus.COMPLETED: "🟢",
                    OrderStatus.CANCELLED: "🔴"
                }
                
                with st.expander(f"{status_color.get(order.status, '⚪')} Order #{order.id} - ${order.total_amount:.2f}"):
                    st.write(f"**Status:** {order.status.value.title()}")
                    st.write(f"**Date:** {order.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Items:** {len(order.order_items)}")
        else:
            st.info("No orders yet. Visit the Marketplace to order products!")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔬 Scan Plant Disease", use_container_width=True):
            st.session_state.page = 'disease_detection'
            st.rerun()
    
    with col2:
        if st.button("🛒 Browse Products", use_container_width=True):
            st.session_state.page = 'marketplace'
            st.rerun()
    
    with col3:
        if st.button("🤖 Ask AI Assistant", use_container_width=True):
            st.session_state.page = 'ai_assistant'
            st.rerun()
    
    with col4:
        if st.button("👥 Join Community", use_container_width=True):
            st.session_state.page = 'community'
            st.rerun()
