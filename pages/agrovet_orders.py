import streamlit as st
from database import Order, OrderStatus
from sqlalchemy import desc

def show():
    if not st.session_state.user:
        st.warning("Please login to manage orders")
        return
    
    st.markdown('<div class="main-header"><h1>📦 Order Management</h1><p>Process and track customer orders</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2, tab3, tab4 = st.tabs(["🟡 Pending", "🔵 Processing", "✅ Completed", "📋 All Orders"])
    
    with tab1:
        show_orders(db, OrderStatus.PENDING)
    
    with tab2:
        show_orders(db, OrderStatus.PROCESSING)
    
    with tab3:
        show_orders(db, OrderStatus.COMPLETED)
    
    with tab4:
        show_orders(db, None)

def show_orders(db, status_filter=None):
    """Display orders with optional status filter"""
    
    query = db.query(Order).filter(Order.agrovet_id == st.session_state.user.id)
    
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
                    st.write(f"**Customer:** {order.farmer.full_name if order.farmer else 'Walk-in Customer'}")
                    if order.farmer:
                        st.write(f"**Phone:** {order.farmer.phone}")
                        st.write(f"**Location:** {order.farmer.location}")
                    st.write(f"**Order Date:** {order.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Total Amount:** ${order.total_amount:.2f}")
                
                with col2:
                    st.write(f"**Current Status:** {order.status.value.title()}")
                    st.write(f"**Delivery Address:**")
                    st.write(order.delivery_address or "In-store pickup")
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
                
                st.markdown("---")
                
                col_status, col_actions = st.columns([2, 2])
                
                with col_status:
                    new_status = st.selectbox(
                        "Update Status",
                        [status.value for status in OrderStatus],
                        index=[status.value for status in OrderStatus].index(order.status.value),
                        key=f"status_{order.id}"
                    )
                
                with col_actions:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("💾 Update Order", key=f"update_{order.id}"):
                        order.status = OrderStatus(new_status)
                        db.commit()
                        st.success(f"Order #{order.id} updated to {new_status}!")
                        st.rerun()
    else:
        st.info("No orders found")
