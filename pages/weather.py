import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show():
    if not st.session_state.user:
        st.warning("Please login to access weather information")
        return
    
    st.markdown('<div class="main-header"><h1>🌦️ Weather & Crop Calendar</h1><p>Plan your farming activities with weather forecasts</p></div>', unsafe_allow_html=True)
    
    st.info(f"📍 Weather forecast for: **{st.session_state.user.location}**")
    
    tab1, tab2 = st.tabs(["🌤️ 7-Day Forecast", "📅 Crop Calendar"])
    
    with tab1:
        show_weather_forecast()
    
    with tab2:
        show_crop_calendar()

def show_weather_forecast():
    """Display weather forecast"""
    st.markdown("### 7-Day Weather Forecast")
    
    cols = st.columns(7)
    
    for i, col in enumerate(cols):
        with col:
            date = datetime.now() + timedelta(days=i)
            day_name = date.strftime("%a")
            
            temp = random.randint(20, 35)
            condition = random.choice(["☀️ Sunny", "⛅ Partly Cloudy", "☁️ Cloudy", "🌧️ Rainy"])
            
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h4>{day_name}</h4>
                <p style='font-size: 2rem;'>{condition.split()[0]}</p>
                <h3>{temp}°C</h3>
                <p>{condition.split()[1] if len(condition.split()) > 1 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Temperature Trend")
    days = [(datetime.now() + timedelta(days=i)).strftime("%a %d") for i in range(7)]
    temps = [random.randint(20, 35) for _ in range(7)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temps, mode='lines+markers', name='Temperature',
                             line=dict(color='#16a34a', width=3), marker=dict(size=10)))
    fig.update_layout(title="7-Day Temperature Forecast", xaxis_title="Day", yaxis_title="Temperature (°C)",
                      height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🌾 Farming Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Good for:**
        - Planting seedlings
        - Applying fertilizers
        - Harvesting mature crops
        - Field preparation
        """)
    
    with col2:
        st.warning("""
        **⚠️ Avoid:**
        - Spraying pesticides on rainy days
        - Irrigation during heavy rain periods
        - Outdoor storage of harvested crops
        """)

def show_crop_calendar():
    """Display crop planting and harvesting calendar"""
    st.markdown("### 📅 Seasonal Crop Calendar")
    
    current_month = datetime.now().strftime("%B")
    st.info(f"Current Month: **{current_month}**")
    
    st.markdown("#### 🌱 Recommended Crops to Plant This Month")
    
    crops_to_plant = [
        {"name": "Tomatoes", "days_to_harvest": "60-80", "difficulty": "Easy"},
        {"name": "Lettuce", "days_to_harvest": "30-45", "difficulty": "Easy"},
        {"name": "Carrots", "days_to_harvest": "70-80", "difficulty": "Medium"},
        {"name": "Peppers", "days_to_harvest": "60-90", "difficulty": "Medium"},
    ]
    
    cols = st.columns(2)
    for idx, crop in enumerate(crops_to_plant):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='product-card'>
                <h4>🌿 {crop['name']}</h4>
                <p>⏱️ Days to Harvest: {crop['days_to_harvest']}</p>
                <p>📊 Difficulty: {crop['difficulty']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 🌾 Crops Ready for Harvest")
    
    harvest_crops = [
        {"name": "Wheat", "planted": "3 months ago", "yield_estimate": "High"},
        {"name": "Corn", "planted": "4 months ago", "yield_estimate": "Medium"},
    ]
    
    for crop in harvest_crops:
        st.success(f"**{crop['name']}** - Planted {crop['planted']} | Expected Yield: {crop['yield_estimate']}")
    
    st.markdown("---")
    
    st.markdown("#### 🔔 Upcoming Activities")
    
    activities = [
        {"date": "Tomorrow", "activity": "Apply fertilizer to tomato plants", "priority": "High"},
        {"date": "In 3 days", "activity": "Check irrigation system", "priority": "Medium"},
        {"date": "Next week", "activity": "Harvest lettuce crop", "priority": "High"},
    ]
    
    for activity in activities:
        priority_color = "#ef4444" if activity['priority'] == "High" else "#f59e0b"
        st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {priority_color};'>
            <strong>{activity['date']}</strong>: {activity['activity']} 
            <span style='color: {priority_color}; font-weight: bold;'>({activity['priority']} Priority)</span>
        </div>
        """, unsafe_allow_html=True)
