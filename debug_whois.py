import whois
import re
from datetime import datetime

def test_domain(url):
    print(f"Testing URL: {url}")
    # Improved regex to handle URLs without http
    if not url.startswith("http"):
        url = "https://" + url
        
    domain_match = re.search(r'https?://(?:www\.)?([\w\-.]+)', url)
    if not domain_match:
        print("Regex failed to match domain.")
        return

    domain = domain_match.group(1)
    print(f"Extracted Domain: {domain}")
    
    try:
        w = whois.whois(domain)
        print(f"Whois Result type: {type(w)}")
        print(f"Creation Date: {w.creation_date} (Type: {type(w.creation_date)})")
        
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            print(f"Fixed List Date: {creation_date}")
            
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            print(f"Age in days: {age_days}")
        else:
            print("No creation date found.")
            
    except Exception as e:
        print(f"Whois Error: {e}")

print("--- TEST 1 ---")
test_domain("google.com")
print("\n--- TEST 2 ---")
test_domain("https://www.google.com/")

