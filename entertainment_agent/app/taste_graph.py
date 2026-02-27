"""Taste profile visualization components."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_taste_profile(memory_manager):
    """
    Render the taste profile visualization in the sidebar.
    
    Args:
        memory_manager: MemoryManager instance to load weight data
    """
    with st.sidebar:
        st.header("Your Taste Profile")
        
        # Load current memory data
        current_weights = memory_manager.get_weights()
        
        if current_weights:
            # Convert dict to DataFrame for plotting
            df_weights = pd.DataFrame(list(current_weights.items()), columns=['Theme', 'Weight'])
            df_weights = df_weights.sort_values(by='Weight', ascending=False).head(10)
            
            # Create a horizontal bar chart
            fig = px.bar(df_weights, x='Weight', y='Theme', orientation='h', 
                         color='Weight', color_continuous_scale='Reds',
                         template="plotly_dark")
            
            fig.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No memory data yet. Start liking items to build your profile!")
