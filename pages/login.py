import streamlit as st
from auth import authenticate_user

def show():
    st.markdown('<div class="main-header"><h1>🔑 Login to Adiseware</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    user, error = authenticate_user(st.session_state.db, username, password)
                    
                    if error:
                        st.error(f"Login failed: {error}")
                    else:
                        st.session_state.user = user
                        st.success(f"Welcome back, {user.full_name}!")
                        st.balloons()
                        
                        if user.role.value == 'farmer':
                            st.session_state.page = 'farmer_dashboard'
                        elif user.role.value == 'agrovet':
                            st.session_state.page = 'agrovet_dashboard'
                        else:
                            st.session_state.page = 'home'
                        
                        st.rerun()
        
        st.markdown("---")
        st.info("Don't have an account? Click 'Register' in the sidebar to create one.")
