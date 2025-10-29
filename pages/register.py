import streamlit as st
from auth import create_user
from database import UserRole

def show():
    st.markdown('<div class="main-header"><h1>📝 Register for Adiseware</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Create Your Account")
        
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            username = st.text_input("Username", placeholder="johndoe")
            email = st.text_input("Email", placeholder="john@example.com")
            phone = st.text_input("Phone Number", placeholder="+1234567890")
            password = st.text_input("Password", type="password", placeholder="Enter a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            role = st.selectbox("I am a:", ["Farmer", "Agrovet Owner/Manager"])
            location = st.text_input("Location", placeholder="City, Country")
            
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if not all([full_name, username, email, phone, password, confirm_password, location]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    user_role = UserRole.FARMER if role == "Farmer" else UserRole.AGROVET
                    
                    user, error = create_user(
                        st.session_state.db,
                        username=username,
                        email=email,
                        password=password,
                        full_name=full_name,
                        phone=phone,
                        role=user_role,
                        location=location
                    )
                    
                    if error:
                        st.error(f"Registration failed: {error}")
                    else:
                        st.success(f"Account created successfully! Welcome, {full_name}!")
                        st.balloons()
                        st.info("Please login with your credentials to continue.")
                        
                        if st.button("Go to Login"):
                            st.session_state.page = 'login'
                            st.rerun()
        
        st.markdown("---")
        st.info("Already have an account? Click 'Login' in the sidebar.")
