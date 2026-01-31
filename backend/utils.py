import re
import whois
from datetime import datetime
from pypdf import PdfReader
from googlesearch import search
import streamlit as st
from backend.config import SCAM_KEYWORDS

# This handles all the heavy lifting for checking scams

def scan_for_keywords(text):
    # Checks if any bad words are in the text
    found = []
    text_lower = text.lower()
    for keyword in SCAM_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)
    return found

def extract_text_from_pdf(file):
    # Grabs text from the PDF file
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
    # Figures out how old a website is
    try:
        domain_match = re.search(r'https?://(?:www\.)?([\w\-.]+)', url)
        if not domain_match:
            return "Invalid URL", 0
        domain = domain_match.group(1)
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        # Sometimes whois returns a list, sometimes a date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not creation_date:
            return "Unknown", 0
            
        age_days = (datetime.now() - creation_date).days
        return creation_date.strftime('%Y-%m-%d'), age_days
    except Exception:
        return "Hidden/Error", 0

def check_company_reputation(company_name):
    # Googles the company to see if people say it's a scam
    query = f'"{company_name}" scam review fraud complaints'
    results = []
    try:
        # Search top 3 results
        for j in search(query, num_results=3, advanced=True):
            results.append(f"- [{j.title}]({j.url}): {j.description}")
    except Exception:
        return "⚠️ Could not verify company reputation online (Network/API Limit)."
    return "\n".join(results) if results else "No specific scam reports found."
