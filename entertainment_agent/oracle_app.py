"""Main Streamlit application for the Entertainment Oracle."""

from core.brain import EntertainmentBrain
from core.dispatcher import ToolDispatcher
from ui.templates import STYLES_CSS, get_badge_html
from app.taste_graph import render_taste_profile

import streamlit as st


def render_main_app():
    """Main application UI rendering logic."""
    st.markdown(STYLES_CSS, unsafe_allow_html=True)
    
    # Setup the Brain and Dispatcher
    brain = EntertainmentBrain()
    dispatcher = ToolDispatcher()
    
    st.set_page_config(page_title="Entertainment Oracle", layout="wide")
    
    st.title("Entertainment Oracle")
    st.caption("Map your Taste Graph across the Multimedia Universe")
    
    # Render sidebar with taste profile
    render_taste_profile(brain.memory)
    
    # 1. Input Section
    user_input = st.text_input("Tell me something you liked recently and why:", 
                              placeholder="I loved 'The Bear' because of the high-stress professionalism...")
    
    if st.button("Generate Taste Grid"):
        if user_input:
            with st.spinner("Analyzing traits and querying APIs..."):
                # 2. Process through Brain
                raw_response = brain.get_recommendation(user_input)
                
                # 3. Enrich through Dispatcher
                enriched_grid = dispatcher.enrich_grid(raw_response['taste_grid'])
                
                # 4. Display Analysis
                st.subheader("Intelligence Analysis")
                st.write(raw_response['analysis'])
                st.info(f"**Extracted Traits:** {', '.join(raw_response['extracted_traits'])}")
                
                st.divider()
                
                # 5. The 6-Item Grid (using Streamlit columns)
                st.subheader("Your Taste Grid")
                # Create two rows of three columns
                rows = [st.columns(3), st.columns(3)]
                flat_cols = [col for row in rows for col in row]
                for i, item in enumerate(enriched_grid):
                    with flat_cols[i]:
                        st.markdown(f"### {item['media_type']}")
                        if item.get('metadata') and item['metadata'].get('image'):
                            st.image(item['metadata']['image'])
                        st.write(f"**{item['title']}**")
        
                        # Create a row of badges
                        if item.get('metadata'):
                            badge_html = get_badge_html(item['metadata'])
                            st.markdown(badge_html, unsafe_allow_html=True)
        
                        # Display Metadata from our ToolDispatcher
                        if item.get('metadata'):
                            meta = item['metadata']
                            # Handle different metadata structures from our APIs
                            if 'overview' in meta: # Movie/TV
                                st.caption(meta['overview'])
                            elif 'artist' in meta: # Music/Podcast
                                st.caption(f"By {meta['artist']}")
                            elif 'authors' in meta: # Books
                                st.caption(f"By {', '.join(meta['authors'])}")
                        
                        st.write(f"*{item['reasoning']}*")
        else:
            st.warning("Please enter a 'Like' to begin.")


# Entry point for Streamlit
render_main_app()
