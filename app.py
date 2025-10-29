import streamlit as st
import os
from database import init_db, SessionLocal, UserRole
from auth import authenticate_user, create_user
import importlib

st.set_page_config(
    page_title="Adiseware - Agricultural Management Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'db' not in st.session_state:
    init_db()
    st.session_state.db = SessionLocal()

if 'user' not in st.session_state:
    st.session_state.user = None

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def logout():
    st.session_state.user = None
    st.session_state.page = 'home'
    st.rerun()

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #16a34a;
    }
    .nav-button {
        width: 100%;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #dcfce7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #16a34a;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #fee2e2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    .product-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌱 Adiseware")
    st.markdown("---")
    
    if st.session_state.user:
        st.markdown(f"**Welcome, {st.session_state.user.full_name}**")
        st.markdown(f"*Role: {st.session_state.user.role.value.title()}*")
        st.markdown("---")
        
        if st.session_state.user.role == UserRole.FARMER:
            st.markdown("#### Farmer Menu")
            if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
                set_page('farmer_dashboard')
            if st.button("🔬 Disease Detection", key="nav_detection", use_container_width=True):
                set_page('disease_detection')
            if st.button("🛒 Marketplace", key="nav_marketplace", use_container_width=True):
                set_page('marketplace')
            if st.button("📦 My Orders", key="nav_orders", use_container_width=True):
                set_page('my_orders')
            if st.button("👥 Community", key="nav_community", use_container_width=True):
                set_page('community')
            if st.button("🤖 AI Assistant", key="nav_ai", use_container_width=True):
                set_page('ai_assistant')
            if st.button("🌦️ Weather", key="nav_weather", use_container_width=True):
                set_page('weather')
                
        elif st.session_state.user.role == UserRole.AGROVET:
            st.markdown("#### Agrovet Menu")
            if st.button("🏠 Dashboard", key="nav_agrovet_dashboard", use_container_width=True):
                set_page('agrovet_dashboard')
            if st.button("💰 POS System", key="nav_pos", use_container_width=True):
                set_page('pos_system')
            if st.button("📦 Orders", key="nav_agrovet_orders", use_container_width=True):
                set_page('agrovet_orders')
            if st.button("📊 Inventory", key="nav_inventory", use_container_width=True):
                set_page('inventory')
            if st.button("👥 CRM", key="nav_crm", use_container_width=True):
                set_page('crm')
            if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
                set_page('analytics')
            if st.button("👥 Community", key="nav_community_av", use_container_width=True):
                set_page('community')
        
        elif st.session_state.user.role == UserRole.ADMIN:
            st.markdown("#### Admin Menu")
            if st.button("🏠 Dashboard", key="nav_admin_dashboard", use_container_width=True):
                set_page('admin_dashboard')
            if st.button("👥 User Management", key="nav_users", use_container_width=True):
                set_page('user_management')
            if st.button("📦 All Orders", key="nav_all_orders", use_container_width=True):
                set_page('all_orders')
            if st.button("🏪 All Products", key="nav_all_products", use_container_width=True):
                set_page('all_products')
            if st.button("📊 System Analytics", key="nav_system_analytics", use_container_width=True):
                set_page('system_analytics')
            if st.button("👥 Community", key="nav_community_admin", use_container_width=True):
                set_page('community')
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    else:
        st.markdown("#### Welcome")
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            set_page('home')
        if st.button("🔑 Login", key="nav_login", use_container_width=True):
            set_page('login')
        if st.button("📝 Register", key="nav_register", use_container_width=True):
            set_page('register')

if st.session_state.page == 'home':
    from pages import home
    home.show()
elif st.session_state.page == 'login':
    from pages import login
    login.show()
elif st.session_state.page == 'register':
    from pages import register
    register.show()
elif st.session_state.page == 'farmer_dashboard':
    from pages import farmer_dashboard
    farmer_dashboard.show()
elif st.session_state.page == 'disease_detection':
    from pages import disease_detection
    disease_detection.show()
elif st.session_state.page == 'marketplace':
    from pages import marketplace
    marketplace.show()
elif st.session_state.page == 'my_orders':
    from pages import my_orders
    my_orders.show()
elif st.session_state.page == 'community':
    from pages import community
    community.show()
elif st.session_state.page == 'ai_assistant':
    from pages import ai_assistant
    ai_assistant.show()
elif st.session_state.page == 'weather':
    from pages import weather
    weather.show()
elif st.session_state.page == 'agrovet_dashboard':
    from pages import agrovet_dashboard
    agrovet_dashboard.show()
elif st.session_state.page == 'pos_system':
    from pages import pos_system
    pos_system.show()
elif st.session_state.page == 'agrovet_orders':
    from pages import agrovet_orders
    agrovet_orders.show()
elif st.session_state.page == 'inventory':
    from pages import inventory
    inventory.show()
elif st.session_state.page == 'crm':
    from pages import crm
    crm.show()
elif st.session_state.page == 'analytics':
    from pages import analytics
    analytics.show()
elif st.session_state.page == 'admin_dashboard':
    from pages import admin_dashboard
    admin_dashboard.show()
elif st.session_state.page == 'user_management':
    from pages import user_management
    user_management.show()
elif st.session_state.page == 'all_orders':
    from pages import all_orders
    all_orders.show()
elif st.session_state.page == 'all_products':
    from pages import all_products
    all_products.show()
elif st.session_state.page == 'system_analytics':
    from pages import system_analytics
    system_analytics.show()
