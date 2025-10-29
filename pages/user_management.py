import streamlit as st
from database import User, UserRole
from auth import create_user
from sqlalchemy import desc

def show():
    if not st.session_state.user or st.session_state.user.role != UserRole.ADMIN:
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.markdown('<div class="main-header"><h1>👥 User Management</h1><p>Manage all platform users</p></div>', unsafe_allow_html=True)
    
    db = st.session_state.db
    
    tab1, tab2 = st.tabs(["👨‍🌾 All Users", "➕ Add New User"])
    
    with tab1:
        show_users(db)
    
    with tab2:
        add_user(db)

def show_users(db):
    """Display all users"""
    
    st.markdown("### User Database")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search users", placeholder="Search by name, username, email...")
    
    with col2:
        role_filter = st.selectbox("Role", ["All", "Farmer", "Agrovet", "Admin"])
    
    with col3:
        status_filter = st.selectbox("Status", ["Active", "Inactive", "All"])
    
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | 
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    if role_filter != "All":
        query = query.filter(User.role == UserRole[role_filter.upper()])
    
    if status_filter == "Active":
        query = query.filter(User.is_active == True)
    elif status_filter == "Inactive":
        query = query.filter(User.is_active == False)
    
    users = query.order_by(desc(User.created_at)).all()
    
    if users:
        for user in users:
            status_icon = "✅" if user.is_active else "❌"
            role_icon = {"farmer": "👨‍🌾", "agrovet": "🏪", "admin": "🔧"}
            
            with st.expander(f"{status_icon} {role_icon.get(user.role.value, '👤')} {user.full_name} ({user.username})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Username:** {user.username}")
                    st.write(f"**Email:** {user.email}")
                    st.write(f"**Phone:** {user.phone}")
                    st.write(f"**Location:** {user.location}")
                
                with col2:
                    st.write(f"**Role:** {user.role.value.title()}")
                    st.write(f"**Status:** {'Active' if user.is_active else 'Inactive'}")
                    st.write(f"**Joined:** {user.created_at.strftime('%Y-%m-%d')}")
                
                st.markdown("---")
                
                col_status, col_delete = st.columns(2)
                
                with col_status:
                    new_status = st.checkbox("Active", value=user.is_active, key=f"status_{user.id}")
                    if new_status != user.is_active:
                        if st.button("💾 Update Status", key=f"update_status_{user.id}"):
                            user.is_active = new_status
                            db.commit()
                            st.success(f"User status updated!")
                            st.rerun()
                
                with col_delete:
                    if st.button("🗑️ Delete User", key=f"delete_{user.id}"):
                        db.delete(user)
                        db.commit()
                        st.success("User deleted!")
                        st.rerun()
    else:
        st.info("No users found")

def add_user(db):
    """Add new user form"""
    
    st.markdown("### Create New User Account")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            username = st.text_input("Username *")
            email = st.text_input("Email *")
            phone = st.text_input("Phone Number *")
        
        with col2:
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            role = st.selectbox("Role *", ["Farmer", "Agrovet", "Admin"])
            location = st.text_input("Location")
        
        submit = st.form_submit_button("➕ Create User", use_container_width=True)
        
        if submit:
            if not all([full_name, username, email, phone, password, confirm_password]):
                st.error("Please fill in all required fields (*)")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                user_role = UserRole[role.upper()]
                
                user, error = create_user(
                    db,
                    username=username,
                    email=email,
                    password=password,
                    full_name=full_name,
                    phone=phone,
                    role=user_role,
                    location=location
                )
                
                if error:
                    st.error(f"Failed to create user: {error}")
                else:
                    st.success(f"✅ User '{full_name}' created successfully!")
                    st.balloons()
