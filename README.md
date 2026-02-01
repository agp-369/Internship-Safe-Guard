# Internship Safe-Guard 🛡️

Hey, welcome to our project for the **Build4Students Hackathon 2026!**

We built this tool because student scams are getting crazy. You get an email offering $50/hr for "data entry," and next thing you know, your bank account is drained. This app stops that.

**[👉 Live Demo Here](https://share.streamlit.io/your-username/your-repo-name)** (Update this link after you deploy!)

## What it does
It's basically a personal cybersecurity analyst.
1. You upload an offer letter or paste a weird URL.
2. We run some python scripts to check if the website was created like... yesterday (huge red flag).
3. We check for keywords like "wire transfer" or "kindly".
4. Then we ask Google's Gemini AI to look at all the evidence and give you a verdict: Safe or Scam.

## Project Structure
We organized the code to be clean but also easy to deploy.

* **`backend/`**: Contains the core logic and forensic tools.
* **`ui/`**: Handles the styling and frontend components.
* **`streamlit/`**: Contains the **deployment-ready** version of the app (all-in-one file for Streamlit Cloud).

## How to run it locally

1. **Clone it:**
   ```bash
   git clone https://github.com/your-username/Internship-Safe-Guard.git
   cd Internship-Safe-Guard
   ```

2. **Install the python stuff:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get an API Key:**
   You need a Google Gemini API key. Put it in a `.env` file like this:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

4. **Run the app:**
   ```bash
   streamlit run streamlit/app.py
   ```

## Tech we used
* Python (obv)
* Streamlit (for the frontend)
* Google Gemini (for the brains)

---
*Stay safe out there!*