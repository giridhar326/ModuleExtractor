# Pulse Module Extractor

An AI-powered Streamlit web app that crawls help documentation websites and extracts structured **modules**, **submodules**, and their descriptions. Built to fulfill the Pulse-AI assignment requirements.

---
## Features

* Accepts any help documentation URL
* Recursively crawls linked pages (up to 5 per domain)
* Identifies major modules and related submodules
* Extracts detailed descriptions for each
* Supports JavaScript-rendered pages using Selenium
* Outputs structured JSON
* Interactive UI with Streamlit
* Allows users to download results

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/pulse-module-extractor.git
cd pulse-module-extractor
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

---

##  URLs to Test

* [https://help.zluri.com/](https://help.zluri.com/)
* [https://wordpress.org/documentation/](https://wordpress.org/documentation/)
* [https://support.freshdesk.com/en/support/home](https://support.freshdesk.com/en/support/home)
* [https://www.chargebee.com/docs/2.0/](https://www.chargebee.com/docs/2.0/)
* [https://knowledge.hubspot.com/](https://knowledge.hubspot.com/)


---

## Project Structure

```
pulse-module-extractor/
├── module_extractor.py         # Core crawler and parser
├── streamlit_app.py            # Web app interface
├── output_zluri.json           # Sample output 1
├── output_wp.json              # Sample output 2
├── output_freshdesk.json       # Sample output 3
├── output_chargebee.json       # Sample output 4
├── output_hubspot.json         # Sample output 5
├── README.md                   # You're looking at it
├── requirements.txt            # Python dependencies
└── .gitignore                  # Ignores venv and pycache
```

---

## Output Format

```json
[
  {
    "module": "Account Settings",
    "Description": "Tools to manage profile and security settings.",
    "Submodules": {
      "Change Email": "Steps to update your email address.",
      "Two-Factor Authentication": "How to set up 2FA."
    }
  }
]
```

---

## Demo Video

Watch the walkthrough video: (https://drive.google.com/file/d/1XWKnslFRcYfYjESIjuczhio0gMPgWG1q/view?usp=sharing)

---

## Technologies Used

* Python
* Streamlit
* Requests
* BeautifulSoup4
* Selenium (with ChromeDriver)
* lxml

---


This project was tested on:

* [https://help.zluri.com/](https://help.zluri.com/)
* [https://wordpress.org/documentation/](https://wordpress.org/documentation/)
* [https://support.freshdesk.com/en/support/home](https://support.freshdesk.com/en/support/home)
* [https://www.chargebee.com/docs/2.0/](https://www.chargebee.com/docs/2.0/)
* [https://knowledge.hubspot.com/](https://knowledge.hubspot.com/)

Each test generated a valid structured JSON output demonstrating module and submodule extraction.
---

