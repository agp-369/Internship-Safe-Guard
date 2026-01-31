import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Importing from our organised folders
from backend.config import PAGE_TITLE, PAGE_ICON
from ui.styles import inject_custom_css, render_header
from backend.utils import (
    scan_for_keywords,
    extract_text_from_pdf,
    check_domain_age,
    check_company_reputation
)

# Load environment variables
load_dotenv()

# --- SETUP & CONFIGURATION ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

# Secure API Key Loading
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Updated to latest stable model (Gemini 2.5 Flash)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None


# --- MAIN APPLICATION LOGIC ---
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
            if age < 180:
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
        
        if not model:
            st.error("Cannot run scan without API Key.")
            return

        with st.spinner("🕵️‍♂️ Analyzing patterns, checking forensics, and consulting security database..."):
            try:
                prompt = f"""
                You are 'Sentinel', a Senior Cybersecurity Analyst for a University.
                
                MISSION: Analyze this student internship/job lead to detect fraud.
                
                --- INPUT DATA ---
                {input_text}
                
                --- FORENSIC EVIDENCE (FACTS) ---
                {forensic_context}
                
                --- INSTRUCTIONS ---
                1. ANALYZE: Check for red flags (urgency, bad grammar, too good to be true, gmail/yahoo domains for businesses).
                2. VERIFY: Use the provided Forensic Evidence to support your claim.
                3. EDUCATE: Explain WHY something is suspicious so the student learns.
                
                --- OUTPUT FORMAT (Markdown) ---
                ## 🛡️ Analysis Result
                **Verdict:** [SAFE / SUSPICIOUS / HIGH RISK SCAM]  
                **Confidence:** [High/Medium/Low]
                
                ### 🚩 Red Flags Detected:
                * [Bullet point]
                * [Bullet point]
                
                ### ℹ️ Forensic Insight:
                [Discuss the domain age or web reputation if data is available]
                
                ### 🎓 Expert Recommendation:
                [Clear, actionable advice. E.g., "Do not pay money," "Verify on LinkedIn"]
                """
                
                response = model.generate_content(prompt)
                
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Scan interrupted. Error: {str(e)}")
                st.info("Tip: Check your internet connection or API Key.")

    st.markdown("<br><br><div style='text-align: center; opacity: 0.5; font-size: 0.8rem;'>Built for Build4Students Hackathon 2026 • Powered by Gemini</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()