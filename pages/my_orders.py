import streamlit as st
from database import Order, OrderStatus
from sqlalchemy import desc

def show():
    if not st.session_state.user:
        st.warning("Please login to view your orders")
        return
    
    st.markdown('<div class="main-header"><h1>📦 My Orders</h1><p>Track and manage your product orders</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2, tab3 = st.tabs(["📋 All Orders", "🟡 Pending", "✅ Completed"])
    
    with tab1:
        show_orders(db, None)
    
    with tab2:
        show_orders(db, OrderStatus.PENDING)
    
    with tab3:
        show_orders(db, OrderStatus.COMPLETED)

def show_orders(db, status_filter=None):
    """Display orders with optional status filter"""
    
    query = db.query(Order).filter(Order.farmer_id == st.session_state.user.id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.order_by(desc(Order.created_at)).all()
    
    if orders:
        for order in orders:
            status_emoji = {
                OrderStatus.PENDING: "🟡",
                OrderStatus.PROCESSING: "🔵",
                OrderStatus.COMPLETED: "🟢",
                OrderStatus.CANCELLED: "🔴"
            }
            
            with st.expander(f"{status_emoji.get(order.status, '⚪')} Order #{order.id} - ${order.total_amount:.2f} - {order.created_at.strftime('%Y-%m-%d')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Status:** {order.status.value.title()}")
                    st.write(f"**Order Date:** {order.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Total Amount:** ${order.total_amount:.2f}")
                    st.write(f"**Number of Items:** {len(order.order_items)}")
                
                with col2:
                    st.write(f"**Delivery Address:**")
                    st.write(order.delivery_address or "Not specified")
                    if order.notes:
                        st.write(f"**Notes:** {order.notes}")
                
                st.markdown("#### Order Items")
                for item in order.order_items:
                    col_prod, col_qty, col_price, col_total = st.columns([3, 1, 1, 1])
                    with col_prod:
                        st.write(f"**{item.product.name}**")
                    with col_qty:
                        st.write(f"×{item.quantity}")
                    with col_price:
                        st.write(f"${item.unit_price:.2f}")
                    with col_total:
                        st.write(f"${item.subtotal:.2f}")
    else:
        st.info("No orders found")
