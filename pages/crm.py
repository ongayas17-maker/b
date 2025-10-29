import streamlit as st
from database import User, UserRole, Order, CustomerInteraction
from sqlalchemy import func, desc
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to access CRM")
        return
    
    st.markdown('<div class="main-header"><h1>👥 Customer Relationship Management</h1><p>Manage customer interactions and relationships</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2 = st.tabs(["👨‍🌾 Customer List", "📝 Interactions"])
    
    with tab1:
        show_customers(db)
    
    with tab2:
        show_interactions(db)

def show_customers(db):
    """Display customer list with purchase history"""
    
    st.markdown("### Customer Database")
    
    search = st.text_input("🔍 Search customers", placeholder="Search by name, location...")
    
    query = db.query(User).filter(User.role == UserRole.FARMER, User.is_active == True)
    
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | 
            (User.location.ilike(f"%{search}%")) |
            (User.username.ilike(f"%{search}%"))
        )
    
    customers = query.all()
    
    if customers:
        for customer in customers:
            total_orders = db.query(func.count(Order.id)).filter(
                Order.farmer_id == customer.id,
                Order.agrovet_id == st.session_state.user.id
            ).scalar() or 0
            
            total_spent = db.query(func.sum(Order.total_amount)).filter(
                Order.farmer_id == customer.id,
                Order.agrovet_id == st.session_state.user.id
            ).scalar() or 0
            
            with st.expander(f"👤 {customer.full_name} - {total_orders} orders - ${total_spent:.2f} spent"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Username:** {customer.username}")
                    st.write(f"**Email:** {customer.email}")
                    st.write(f"**Phone:** {customer.phone}")
                    st.write(f"**Location:** {customer.location}")
                    st.write(f"**Member Since:** {customer.created_at.strftime('%Y-%m-%d')}")
                
                with col2:
                    st.write(f"**Total Orders:** {total_orders}")
                    st.write(f"**Total Spent:** ${total_spent:.2f}")
                    st.write(f"**Average Order:** ${(total_spent / total_orders if total_orders > 0 else 0):.2f}")
                
                st.markdown("#### Recent Orders")
                recent_orders = db.query(Order).filter(
                    Order.farmer_id == customer.id,
                    Order.agrovet_id == st.session_state.user.id
                ).order_by(desc(Order.created_at)).limit(3).all()
                
                if recent_orders:
                    for order in recent_orders:
                        st.write(f"- Order #{order.id}: ${order.total_amount:.2f} ({order.created_at.strftime('%Y-%m-%d')}) - {order.status.value}")
                else:
                    st.info("No orders yet")
                
                st.markdown("---")
                
                st.markdown("#### Add Interaction Note")
                
                with st.form(f"interaction_{customer.id}"):
                    interaction_type = st.selectbox("Interaction Type", 
                        ["Phone Call", "Email", "In-Person Visit", "Follow-up", "Complaint", "Feedback"],
                        key=f"type_{customer.id}")
                    notes = st.text_area("Notes", placeholder="Record interaction details...", key=f"notes_{customer.id}")
                    
                    if st.form_submit_button("💾 Save Interaction"):
                        if notes:
                            interaction = CustomerInteraction(
                                agrovet_id=st.session_state.user.id,
                                farmer_id=customer.id,
                                interaction_type=interaction_type,
                                notes=notes,
                                created_at=datetime.utcnow()
                            )
                            db.add(interaction)
                            db.commit()
                            st.success("Interaction recorded!")
                            st.rerun()
    else:
        st.info("No customers found")

def show_interactions(db):
    """Display all customer interactions"""
    
    st.markdown("### Recent Interactions")
    
    interactions = db.query(CustomerInteraction).filter(
        CustomerInteraction.agrovet_id == st.session_state.user.id
    ).order_by(desc(CustomerInteraction.created_at)).limit(20).all()
    
    if interactions:
        for interaction in interactions:
            farmer = db.query(User).filter(User.id == interaction.farmer_id).first()
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{farmer.full_name if farmer else 'Unknown'}** - {interaction.interaction_type}")
                    st.write(interaction.notes)
                
                with col2:
                    st.caption(interaction.created_at.strftime('%Y-%m-%d %H:%M'))
                
                st.markdown("---")
    else:
        st.info("No interactions recorded yet")
