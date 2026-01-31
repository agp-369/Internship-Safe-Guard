import streamlit as st
from backend.config import BG_COLOR, THEME_COLOR, SECONDARY_BG, PAGE_TITLE

# This file just handles the way things look. 

def inject_custom_css():
    st.markdown(f"""
    <style>
    /* GLOBAL RESET & BACKGROUND */
    .stApp, body, .stMain {{
        background-color: {BG_COLOR} !important;
    }}
    
    /* UTILITIES */
    header, footer, #MainMenu, div[data-testid="stToolbar"] {{
        visibility: hidden !important;
    }}
    
    /* TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, label, .stCaption, span {{
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* CUSTOM TABS CONTAINER */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 80px; 
        justify-content: center;
        padding-bottom: 15px;
        margin-bottom: 10px;
        border: none !important;
    }}
    
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    
    /* INDIVIDUAL TAB STYLING */
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border: none !important;
        color: #a0aabf;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 10px 0px;
    }}
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {THEME_COLOR} !important;
        font-weight: bold;
        border-bottom: 3px solid {THEME_COLOR} !important;
        border-radius: 0px;
    }}
    
    /* INPUT FIELDS */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stFileUploader {{
        background-color: {SECONDARY_BG} !important;
        color: white !important;
        border: 1px solid #556285 !important;
        border-radius: 8px;
    }}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {THEME_COLOR} !important;
        box-shadow: 0 0 10px rgba(134, 170, 249, 0.4);
    }}
    
    /* PRIMARY ACTION BUTTON STYLING */
    .stButton>button {{
        background-color: {THEME_COLOR} !important; 
        color: {BG_COLOR} !important;             
        border: none !important;  
        border-radius: 50px;
        font-weight: 700;
        padding: 12px 40px !important; 
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
        display: block !important;
        width: 100% !important; /* Fills the column */
    }}
    
    .stButton>button:hover {{
        background-color: #5a8dee !important; 
        color: white !important;
        transform: translateY(-2px); 
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }}

    /* RESULTS CONTAINER */
    .result-box {{
        padding: 25px;
        border-radius: 10px;
        background-color: {SECONDARY_BG};
        border-left: 5px solid {THEME_COLOR};
        margin-top: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    /* LAYOUT CONSTRAINT */
    .block-container {{
        padding-top: 2rem;
        max-width: 800px;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 40px;">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L3 7V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V7L12 2ZM10 17L6 13L7.41 11.59L10 14.17L16.59 7.58L18 9L10 17Z" fill="{THEME_COLOR}"/>
        </svg>
        <h1 style="color: {THEME_COLOR} !important; font-weight: 800; letter-spacing: 2px; margin-top: 15px; font-size: 2.5rem;">{PAGE_TITLE.upper()}</h1>
        <p style="color: #a0aabf; font-size: 1.1rem; max-width: 500px; margin: 0 auto;">
            Protecting students from recruitment fraud using AI & Real-time Forensics.
        </p>
    </div>
    """, unsafe_allow_html=True)
