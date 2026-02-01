import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import re
import whois
from datetime import datetime
from pypdf import PdfReader
from googlesearch import search

# ==========================================
# 1. CONFIGURATION & CONSTANTS
# ==========================================
PAGE_TITLE = "Internship Safe-Guard"
PAGE_ICON = "🛡️"
THEME_COLOR = "#86AAF9"
BG_COLOR = "#3d4a69"
SECONDARY_BG = "#2b3650"

SCAM_KEYWORDS = [
    "kindly", "money order", "check processing", "telegram", "whatsapp", 
    "training fee", "refundable deposit", "google chat interview", 
    "wire transfer", "cashier's check", "urgent response required"
]

# ==========================================
# 2. UTILITY FUNCTIONS
# ==========================================
def scan_for_keywords(text):
    """Checks if any bad words are in the text"""
    found = []
    text_lower = text.lower()
    for keyword in SCAM_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)
    return found

def extract_text_from_pdf(file):
    """Grabs text from the PDF file"""
    try:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content
        return text if text.strip() else None
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def check_domain_age(url):
    """Figures out how old a website is"""
    try:
        # Handle URLs without protocol
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        domain_match = re.search(r'https?://(?:www\.)?([\w\-]+.)', url)
        if not domain_match:
            return "Invalid URL", None
        domain = domain_match.group(1)
        
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        # Sometimes whois returns a list, sometimes a date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not creation_date:
            return "Unknown", None
            
        age_days = (datetime.now() - creation_date).days
        return creation_date.strftime('%Y-%m-%d'), age_days
    except Exception:
        return "Hidden/Error", None

def check_company_reputation(company_name):
    """Googles the company to see if people say it's a scam"""
    query = f'"{company_name}" scam review fraud complaints'
    results = []
    try:
        # Search top 3 results
        for j in search(query, num_results=3, advanced=True):
            results.append(f"- [{j.title}]({j.url}): {j.description}")
    except Exception:
        return "⚠️ Could not verify company reputation online (Network/API Limit)."
    return "\n".join(results) if results else "No specific scam reports found."

# ==========================================
# 3. UI STYLING
# ==========================================
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

# ==========================================
# 4. MAIN APPLICATION LOGIC
# ==========================================

# Load environment variables
load_dotenv()

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

# Secure API Key Loading
api_key = os.getenv("GOOGLE_API_KEY")
client = None

if api_key:
    # Initialize the NEW Google GenAI Client
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.warning(f"Failed to initialize Gemini Client: {e}")
else:
    client = None

def main():
    inject_custom_css()
    render_header()
    
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found. Please set it in your .env file.")
    
    tab_file, tab_url, tab_search = st.tabs(["📄 ANALYZE OFFER", "🌐 CHECK URL", "🔍 INVESTIGATE"])
    
    input_text = ""
    forensic_context = ""
    
    # --- TAB 1: FILE ---
    with tab_file:
        st.caption("Upload an offer letter or contract (PDF/TXT)")
        uploaded_file = st.file_uploader("Drop file here", type=['pdf', 'txt'], label_visibility="collapsed")
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                input_text = extract_text_from_pdf(uploaded_file)
            else:
                input_text = str(uploaded_file.read(), "utf-8")
                
    # --- TAB 2: URL ---
    with tab_url:
        st.caption("Enter the company's career page or home URL")
        url_input = st.text_input("Website URL", placeholder="https://example.com", label_visibility="collapsed")
        if url_input:
            input_text = f"URL to Analyze: {url_input}"
            reg_date, age = check_domain_age(url_input)
            
            if age is None:
                forensic_context += "⚠️ **Warning:** Could not verify domain age (WHOIS lookup failed or timed out).\n"
            elif age < 180:
                forensic_context += f"🚨 **CRITICAL:** Domain is VERY NEW ({age} days old). Real companies usually have older domains.\n"
            else:
                forensic_context += f"✅ **Domain Trust:** Domain is {age} days old (Created {reg_date}).\n"
                
    # --- TAB 3: MANUAL ---
    with tab_search:
        st.caption("Enter details manually if you don't have a file")
        col1, col2 = st.columns(2)
        with col1:
            c_name = st.text_input("Company Name")
        with col2:
            c_email = st.text_input("Recruiter Email")
        raw_msg = st.text_area("Copy-paste Email/Message content here", height=100)
        
        inputs = []
        if c_name:
            inputs.append(f"Company: {c_name}")
            rep = check_company_reputation(c_name)
            forensic_context += f"\n🌍 **Reputation Check for '{c_name}':**\n{rep}\n"
        if c_email:
            inputs.append(f"Email: {c_email}")
        if raw_msg:
            inputs.append(f"Message: {raw_msg}")
        if inputs:
            input_text = "\n".join(inputs)

    # --- EXECUTION ---
    # REAL-TIME FACT CHECKING (Keyword Scan)
    if input_text:
        found_keywords = scan_for_keywords(input_text)
        if found_keywords:
            forensic_context += f"\n🚩 **Keyword Alert:** Found suspicious terms: {', '.join(found_keywords).upper()}. These are common in scams."

    st.markdown("###") # Spacer

    # CENTERED BUTTON LAYOUT
    b_col1, b_col2, b_col3 = st.columns([1.2, 2, 0.8])
    with b_col2:
        run_scan = st.button("RUN SECURITY SCAN")

    if run_scan:
        if not input_text:
            st.warning("⚠️ Please provide input in one of the tabs above to start the scan.")
            return
        
        if not client:
            st.error("Cannot run scan without API Key.")
            return

        with st.spinner("🕵️‍♂️ Analyzing patterns, checking forensics, and consulting security database..."):
            try:
                prompt_text = f"""
                You are 'Sentinel', a Senior Cybersecurity Analyst for a University.
                
                MISSION: Analyze this student internship/job lead to detect fraud.
                
                --- INPUT DATA ---
                {input_text}
                
                --- FORENSIC EVIDENCE (FACTS) ---
                {forensic_context}
                
                --- INSTRUCTIONS ---
                1. **KNOWLEDGE OVERRIDE:** If the input is a widely known, legitimate company (e.g., Google, Microsoft, Amazon) and the URL is correct, declare it **SAFE** immediately, even if the "Forensic Evidence" says WHOIS failed.
                2. **ANALYZE:** Check for red flags (urgency, bad grammar, "kindly", "wire transfer").
                3. **VERDICT:** Determine the risk level.
                
                --- OUTPUT FORMAT ---
                You must start your response with EXACTLY one of these three lines:
                VERDICT: SAFE
                VERDICT: CAUTION
                VERDICT: SCAM
                
                (Leave one empty line)
                
                ## 🛡️ Analysis Report
                **Confidence:** [High/Medium/Low]
                
                ### 📝 Summary
                [1-2 sentences explaining the verdict clearly]
                
                ### 🚩 Red Flags (If any):
                * [Point 1]
                
                ### 🎓 Recommendation:
                [Actionable advice]
                """
                
                # New Google GenAI API Call Pattern
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=prompt_text
                )
                
                full_text = response.text
                
                # Parse the Verdict
                lines = full_text.split('\n')
                verdict_line = lines[0].strip().upper()
                report_body = "\n".join(lines[1:])
                
                # Display Visual Banner
                if "SAFE" in verdict_line:
                    st.success("✅ **VERDICT: SAFE**\n\nThis appears to be a legitimate opportunity.")
                elif "SCAM" in verdict_line:
                    st.error("🚨 **VERDICT: HIGH RISK SCAM**\n\nDo not interact. This has multiple signs of fraud.")
                elif "CAUTION" in verdict_line:
                    st.warning("⚠️ **VERDICT: CAUTION**\n\nSome risks detected. Verify carefully before proceeding.")
                else:
                    st.info(f"ℹ️ **VERDICT: UNKNOWN**\n\n{verdict_line}")

                # Display the rest of the report
                st.markdown(f'<div class="result-box">{report_body}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Scan interrupted. Error: {str(e)}")
                st.info("Tip: Check your internet connection or API Key.")

    st.markdown("<br><br><div style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>Built for Build4Students Hackathon 2026 • Powered by Gemini 2.0</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
