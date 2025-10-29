import streamlit as st
from streamlit_camera_input_live import camera_input_live
from PIL import Image
import io
from ai_helper import analyze_plant_disease, search_product_images
from database import DiseaseDetection
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to use disease detection")
        return
    
    st.markdown('<div class="main-header"><h1>🔬 AI Plant Disease Detection</h1><p>Upload or capture plant photos for instant disease diagnosis</p></div>', unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Take clear, well-lit photos of affected plant parts for best results. The AI will analyze the image and provide detailed diagnosis and treatment recommendations.")
    
    tab1, tab2 = st.tabs(["📸 Camera Capture", "📤 Upload Image"])
    
    with tab1:
        st.markdown("### Use Your Camera")
        st.write("Click the button below to take a photo of your plant:")
        
        image = camera_input_live()
        
        if image:
            st.image(image, caption="Captured Plant Image", use_container_width=True)
            
            if st.button("🔍 Analyze This Image", key="analyze_camera", type="primary", use_container_width=True):
                analyze_image(image)
    
    with tab2:
        st.markdown("### Upload an Image")
        uploaded_file = st.file_uploader("Choose a plant image...", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Plant Image", use_container_width=True)
            
            if st.button("🔍 Analyze This Image", key="analyze_upload", type="primary", use_container_width=True):
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                analyze_image(img_byte_arr)

def analyze_image(image_data):
    """Analyze the plant image and display results"""
    
    with st.spinner("🔬 Analyzing plant image with AI... This may take a moment."):
        if isinstance(image_data, bytes):
            image_bytes = image_data
        else:
            image_bytes = image_data.getvalue()
        
        result = analyze_plant_disease(image_bytes)
    
    if "error" in result and result.get("confidence", 0) == 0:
        st.error(f"❌ Analysis Error: {result.get('symptoms', 'Unknown error')}")
        return
    
    st.success("✅ Analysis Complete!")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## 🌿 {result.get('plant_type', 'Plant')}")
        
        disease = result.get('disease_name', 'Unknown')
        confidence = result.get('confidence', 0)
        severity = result.get('severity', 'Unknown')
        
        if disease.lower() == 'healthy':
            st.markdown(f"### ✅ Status: **{disease}**")
            st.success(f"Confidence: {confidence*100:.1f}%")
        else:
            st.markdown(f"### ⚠️ Disease Detected: **{disease}**")
            st.warning(f"Confidence: {confidence*100:.1f}% | Severity: **{severity}**")
    
    with col2:
        confidence_pct = confidence * 100
        color = "#16a34a" if confidence_pct > 80 else "#f59e0b" if confidence_pct > 60 else "#ef4444"
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: {color}; color: white; border-radius: 10px;'>
            <h1>{confidence_pct:.1f}%</h1>
            <p>Confidence Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Symptoms", "🦠 Causes", "💊 Treatment", "🛡️ Prevention"])
    
    with tab1:
        st.markdown("### Observed Symptoms")
        st.write(result.get('symptoms', 'No symptoms information available'))
    
    with tab2:
        st.markdown("### Disease Causes")
        st.write(result.get('causes', 'No causes information available'))
    
    with tab3:
        st.markdown("### Treatment Recommendations")
        st.write(result.get('treatment', 'No treatment information available'))
        
        recommended_products = result.get('recommended_products', [])
        if recommended_products:
            st.markdown("#### 💊 Recommended Products")
            cols = st.columns(min(3, len(recommended_products)))
            for idx, product in enumerate(recommended_products[:3]):
                with cols[idx]:
                    st.markdown(f"**{product}**")
                    st.image(search_product_images(product), use_container_width=True)
                    if st.button(f"🛒 Find in Marketplace", key=f"product_{idx}"):
                        st.session_state.page = 'marketplace'
                        st.rerun()
    
    with tab4:
        st.markdown("### Prevention Measures")
        st.write(result.get('prevention', 'No prevention information available'))
    
    if st.button("💾 Save This Diagnosis", type="primary", use_container_width=True):
        save_diagnosis(result, image_bytes)

def save_diagnosis(result, image_bytes):
    """Save diagnosis to database"""
    try:
        detection = DiseaseDetection(
            user_id=st.session_state.user.id,
            plant_type=result.get('plant_type', 'Unknown'),
            disease_name=result.get('disease_name', 'Unknown'),
            confidence_score=result.get('confidence', 0),
            severity=result.get('severity', 'Unknown'),
            symptoms=result.get('symptoms', ''),
            causes=result.get('causes', ''),
            treatment=result.get('treatment', ''),
            prevention=result.get('prevention', ''),
            created_at=datetime.utcnow()
        )
        
        st.session_state.db.add(detection)
        st.session_state.db.commit()
        
        st.success("✅ Diagnosis saved successfully! You can view it in your dashboard.")
        
    except Exception as e:
        st.error(f"Error saving diagnosis: {str(e)}")
