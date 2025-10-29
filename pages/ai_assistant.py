import streamlit as st
from ai_helper import get_agricultural_advice

def show():
    if not st.session_state.user:
        st.warning("Please login to use the AI assistant")
        return
    
    st.markdown('<div class="main-header"><h1>🤖 AI Agricultural Assistant</h1><p>Get instant farming advice powered by AI</p></div>', unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.info("💡 Ask me anything about farming, crops, diseases, soil management, irrigation, or agricultural best practices!")
    
    suggested_questions = st.columns(3)
    with suggested_questions[0]:
        if st.button("🌱 Best crops for my region?"):
            ask_question(f"What are the best crops to grow in {st.session_state.user.location}?")
    with suggested_questions[1]:
        if st.button("💧 Irrigation tips?"):
            ask_question("What are the best irrigation practices for sustainable farming?")
    with suggested_questions[2]:
        if st.button("🌾 Harvest timing?"):
            ask_question("How do I know when my crops are ready for harvest?")
    
    st.markdown("---")
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dcfce7, #e2f7e8); padding: 1rem; border-radius: 15px; margin: 10px 0; border-bottom-right-radius: 5px;'>
                    <strong>You:</strong><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 15px; margin: 10px 0; border: 1px solid #e2e8f0; border-bottom-left-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                    <strong>🤖 AI Assistant:</strong><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Your question:", placeholder="Ask anything about farming...", label_visibility="collapsed")
        with col2:
            submit = st.form_submit_button("Send", use_container_width=True)
        
        if submit and user_input:
            ask_question(user_input)

def ask_question(question):
    """Process user question and get AI response"""
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question
    })
    
    context = f"Location: {st.session_state.user.location}, Farmer: {st.session_state.user.full_name}"
    
    with st.spinner("🤔 Thinking..."):
        response = get_agricultural_advice(question, context)
    
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response
    })
    
    st.rerun()
