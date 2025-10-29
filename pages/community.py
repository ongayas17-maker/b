import streamlit as st
from database import CommunityPost, Comment
from sqlalchemy import desc
from datetime import datetime

def show():
    if not st.session_state.user:
        st.warning("Please login to access the community")
        return
    
    st.markdown('<div class="main-header"><h1>👥 Farmer Community</h1><p>Connect, share, and learn from fellow farmers</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📰 Community Feed", "✍️ Create Post"])
    
    with tab1:
        show_feed()
    
    with tab2:
        create_post()

def show_feed():
    """Display community posts"""
    db = st.session_state.db
    
    category_filter = st.selectbox("Filter by Category", ["All", "Question", "Experience", "Tips", "Market Info", "Success Story"])
    
    query = db.query(CommunityPost).order_by(desc(CommunityPost.created_at))
    
    if category_filter != "All":
        query = query.filter(CommunityPost.category == category_filter)
    
    posts = query.all()
    
    if posts:
        for post in posts:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {post.title}")
                    st.caption(f"By {post.author.full_name} · {post.created_at.strftime('%Y-%m-%d %H:%M')} · {post.category or 'General'}")
                
                with col2:
                    st.write(f"❤️ {post.likes_count} likes")
                    st.write(f"💬 {len(post.comments)} comments")
                
                st.write(post.content)
                
                if post.image_url:
                    st.image(post.image_url, use_container_width=True)
                
                col_like, col_comment = st.columns([1, 3])
                
                with col_like:
                    if st.button("❤️ Like", key=f"like_{post.id}"):
                        post.likes_count += 1
                        db.commit()
                        st.rerun()
                
                with col_comment:
                    with st.expander(f"💬 View {len(post.comments)} Comments"):
                        for comment in post.comments:
                            st.write(f"**{comment.author.full_name}** · {comment.created_at.strftime('%Y-%m-%d %H:%M')}")
                            st.write(comment.content)
                            st.markdown("---")
                        
                        comment_text = st.text_area("Add a comment", key=f"comment_{post.id}")
                        if st.button("Post Comment", key=f"post_comment_{post.id}"):
                            if comment_text:
                                new_comment = Comment(
                                    post_id=post.id,
                                    author_id=st.session_state.user.id,
                                    content=comment_text,
                                    created_at=datetime.utcnow()
                                )
                                db.add(new_comment)
                                db.commit()
                                st.success("Comment posted!")
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No posts yet. Be the first to share!")

def create_post():
    """Create a new community post"""
    st.markdown("### Share with the Community")
    
    with st.form("new_post_form"):
        title = st.text_input("Post Title", placeholder="Give your post a catchy title...")
        category = st.selectbox("Category", ["Question", "Experience", "Tips", "Market Info", "Success Story"])
        content = st.text_area("Content", placeholder="Share your thoughts, experiences, or questions...", height=200)
        
        submit = st.form_submit_button("📝 Publish Post", use_container_width=True)
        
        if submit:
            if not title or not content:
                st.error("Please fill in both title and content")
            else:
                db = st.session_state.db
                
                post = CommunityPost(
                    author_id=st.session_state.user.id,
                    title=title,
                    content=content,
                    category=category,
                    created_at=datetime.utcnow()
                )
                
                db.add(post)
                db.commit()
                
                st.success("✅ Post published successfully!")
                st.balloons()
                
                if st.button("View in Feed"):
                    st.rerun()
