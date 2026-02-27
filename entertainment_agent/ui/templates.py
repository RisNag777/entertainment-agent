"""HTML and CSS templates for the Entertainment Oracle UI."""

# CSS Styles for the Streamlit app
STYLES_CSS = """
    <style>
    /* 1. Universal Image Enforcer */
    [data-testid="stImage"] img {
        height: 450px !important;  /* Fixed height for all */
        object-fit: cover;         /* Crops instead of stretching */
        border-radius: 15px;       /* Smooth rounded corners */
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);  /* Soft shadow */
        transition: transform 0.3s ease, box-shadow 0.3s ease; /* Animation prep */
    }

    /* 2. Hover Effect (The "Wow" Factor) */
    [data-testid="stImage"] img:hover {
        transform: scale(1.03);    /* Slight zoom on hover */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5); /* Deeper shadow on hover */
        border-color: #ff4b4b;     /* Optional: Highlight border on hover */
    }

    /* 3. Text Alignment */
    .stMarkdown h3 {
        font-size: 1.1rem !important;
        margin-top: 15px !important;
        color: #ff4b4b; /* Accent color for the Media Type */
    }
    
    .stMarkdown p {
        font-size: 0.95rem;
        line-height: 1.4;
    }
    </style>
    """


def get_badge_html(item_metadata):
    """
    Generate HTML for rating and release date badges.
    
    Args:
        item_metadata: Dictionary containing metadata for an item (may include 'rating' and 'release_date')
    
    Returns:
        HTML string for the badges
    """
    rating = item_metadata.get('rating', 'N/A')
    release_date = item_metadata.get('release_date', '????')
    # Extract year from release_date if it's a full date string
    year = release_date[:4] if release_date and len(release_date) >= 4 else '????'
    
    badge_html = f"""
        <div style="display: flex; gap: 5px; margin-bottom: 10px;">
            <span style="background: #ff4b4b; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem;">
                ★ {rating}
            </span>
            <span style="background: #31333F; color: #dfd8d8; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; border: 1px solid #464855;">
                🗓️ {year}
            </span>
        </div>
    """
    return badge_html
