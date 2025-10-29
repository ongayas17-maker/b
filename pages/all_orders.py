import streamlit as st
from database import Order, OrderStatus
from sqlalchemy import desc

def show():
    if not st.session_state.user or st.session_state.user.role.value != 'admin':
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.markdown('<div class="main-header"><h1>📦 All Orders</h1><p>System-wide order monitoring</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All", "🟡 Pending", "🔵 Processing", "✅ Completed"])
    
    with tab1:
        show_orders(db, None)
    
    with tab2:
        show_orders(db, OrderStatus.PENDING)
    
    with tab3:
        show_orders(db, OrderStatus.PROCESSING)
    
    with tab4:
        show_orders(db, OrderStatus.COMPLETED)

def show_orders(db, status_filter=None):
    """Display all orders with optional status filter"""
    
    query = db.query(Order)
    
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
            
            farmer_name = order.farmer.full_name if order.farmer else "Walk-in Customer"
            agrovet_name = order.agrovet.full_name if order.agrovet else "Direct Sale"
            
            with st.expander(f"{status_emoji.get(order.status, '⚪')} Order #{order.id} - ${order.total_amount:.2f} - {order.created_at.strftime('%Y-%m-%d')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Customer:** {farmer_name}")
                    st.write(f"**Agrovet:** {agrovet_name}")
                    st.write(f"**Order Date:** {order.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Status:** {order.status.value.title()}")
                
                with col2:
                    st.write(f"**Total Amount:** ${order.total_amount:.2f}")
                    st.write(f"**Number of Items:** {len(order.order_items)}")
                    st.write(f"**Delivery Address:** {order.delivery_address or 'N/A'}")
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
