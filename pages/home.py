import streamlit as st

def show():
    st.markdown('<div class="main-header"><h1>🌱 Adiseware - Agricultural Management Platform</h1><p>Empowering Farmers with AI-Powered Agriculture</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔬 AI Disease Detection
        Upload or capture plant photos to instantly identify diseases, get treatment recommendations, and find the right medications.
        """)
    
    with col2:
        st.markdown("""
        ### 🛒 Marketplace
        Browse and order agricultural products, fertilizers, and medications from verified agrovets in your area.
        """)
    
    with col3:
        st.markdown("""
        ### 👥 Community
        Connect with fellow farmers, share experiences, ask questions, and learn from agricultural experts.
        """)
    
    st.markdown("---")
    
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### For Farmers:
        - 📸 **Real-time Disease Detection** - Use your phone camera
        - 💊 **Treatment Recommendations** - Get specific medication suggestions
        - 📱 **AI Agricultural Assistant** - 24/7 farming advice
        - 🌦️ **Weather Forecasts** - Plan your farming activities
        - 📦 **Order Tracking** - Track your product orders
        - 💬 **Community Forum** - Learn and share knowledge
        """)
    
    with col2:
        st.markdown("""
        #### For Agrovets:
        - 💰 **Point of Sale System** - Modern checkout experience
        - 📊 **Inventory Management** - Track stock levels
        - 📦 **Order Management** - Process farmer orders
        - 👥 **CRM System** - Manage customer relationships
        - 📈 **Sales Analytics** - Business insights
        - 🎯 **Customer Targeting** - Reach the right farmers
        """)
    
    st.markdown("---")
    
    st.markdown("## 🚀 Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Step 1:** Create your account as a Farmer or Agrovet")
    
    with col2:
        st.info("**Step 2:** Complete your profile with location details")
    
    with col3:
        st.info("**Step 3:** Start using AI-powered agricultural tools")
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f0fdf4 0%, #e2f7e8 100%); border-radius: 10px;'>
        <h3>Ready to transform your farming experience?</h3>
        <p>Join thousands of farmers and agrovets already using Adiseware</p>
    </div>
    """, unsafe_allow_html=True)
