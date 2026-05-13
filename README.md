<div align="center">

# 🤖 LinkedIn Job Automator

### Automate your job hunt. Apply smarter, not harder.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Gmail](https://img.shields.io/badge/Gmail-SMTP-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Automation-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

</div>

---

## 🚀 Overview

> **LinkedIn Job Automator** is a Python-based automation tool that logs into LinkedIn, scrapes recruiter contact emails from job-related posts, and automatically dispatches personalized job application emails with your resume attached — all in one seamless pipeline.

Job hunting is exhausting. Hours are wasted manually hunting for recruiter emails, crafting repetitive emails, and tracking applications. This tool eliminates that friction by combining **browser automation** (Selenium) with **email delivery** (SMTP) into a single, zero-touch workflow. Fire it up, and let it do the prospecting while you focus on interview prep.

---

## ✨ Features

- 🔐 **Automated LinkedIn Login** — Handles credential-based authentication with smart waits and error recovery.
- 🔍 **Intelligent Job Post Scraping** — Searches LinkedIn posts using targeted keyword queries like `"email me"` and `"drop your resume"` to find recruiters actively seeking candidates.
- 📧 **Regex-Powered Email Extraction** — Parses the entire page's visible text to extract valid email addresses using a battle-tested regular expression pattern.
- 📨 **Automated Email Dispatch** — Sends a professional HTML-formatted application email to every extracted email address via Gmail's SMTP server.
- 📎 **Resume Auto-Attachment** — Attaches your PDF resume to every outgoing email automatically.
- ⏱️ **Rate-Limiting & Anti-Spam Delay** — Adds a 30-second delay between each email to respect server limits and avoid spam flags.
- 🧠 **Graceful Error Handling** — Catches login failures, missing files, and SMTP errors without crashing the entire pipeline.
- 🔄 **End-to-End Pipeline** — Single script execution handles the full flow: Login → Scrape → Extract → Email.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core scripting & logic |
| **Browser Automation** | Selenium WebDriver | LinkedIn login & scraping |
| **Wait Strategy** | `WebDriverWait` + `ExpectedConditions` | Robust element interaction |
| **Email Client** | `smtplib` + `MIME` | SMTP-based email delivery |
| **Pattern Matching** | `re` (Regex) | Email address extraction |
| **Browser Driver** | ChromeDriver | Chrome automation interface |

---

## 📁 Directory Structure

```
linkedin-job-automator/
│
├── Main.py                  # Core automation script (entry point)
├── README.md                # Project documentation
├── .env                     # Stores all secret credentials locally
└── .gitignore               # Lists files Git should not track or push
```

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure you have the following installed before you begin:

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version) → [Download here](https://chromedriver.chromium.org/downloads)
- A Gmail account with a **16-digit App Password** (2FA must be enabled)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/sahuharikishor/linkedin-job-automator.git
cd linkedin-job-automator
```

### Step 2 — Install Dependencies

```bash
pip install selenium
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3 — Configure Your Credentials

Open `Main.py` and fill in your personal details in the configuration section at the top:

```python
# LinkedIn credentials
LINKEDIN_USERNAME = "your_linkedin_email@example.com"
LINKEDIN_PASSWORD = "your_linkedin_password"

# Gmail credentials
SENDER_EMAIL    = "your_gmail@gmail.com"
APP_PASSWORD    = "xxxx xxxx xxxx xxxx"   # 16-digit Google App Password

# Path to your resume
RESUME_FILE_PATH = r"C:\Users\YourName\Documents\Resume.pdf"
```

> ⚠️ **Security Note:** Never commit your real credentials to a public repository. Use environment variables or a `.env` file with `python-dotenv` in production.

### Step 4 — Generate a Gmail App Password

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** if not already on
3. Navigate to **App Passwords**
4. Select App: `Mail` | Device: `Windows Computer`
5. Copy the generated 16-digit password into `APP_PASSWORD`

### Step 5 — Run the Script

```bash
python Main.py
```

### Expected Console Output

```
Starting the browser...
Entering credentials...
Successfully logged in!
Navigating to LinkedIn Posts search for: python developer "email me" OR "drop your resume"
Scrolling to load more data...
Hunting for email addresses using Regex...
Success! Found 4 emails: ['recruiter@company.com', ...]

Closing browser. Moving to Email phase...

========================================
SENDING JOB APPLICATIONS
========================================
Preparing to send email to: recruiter@company.com
Resume attached successfully.
Connecting to Gmail server...
Logging in to Gmail...
Sending email...
Email sent successfully!

All applications sent successfully!
```

---

## 🧩 How It Works — Under the Hood

```
┌─────────────────────────────────────────────────────────┐
│                   EXECUTION PIPELINE                    │
│                                                         │
│  1. login_to_linkedin()                                 │
│     └─ Opens Chrome → navigates to LinkedIn login      │
│     └─ Fills credentials → clicks submit               │
│                                                         │
│  2. search_jobs_and_extract_emails()                    │
│     └─ Builds search URL with targeted keywords        │
│     └─ Scrolls page 5× to load dynamic content        │
│     └─ Extracts all page text via body element         │
│     └─ Applies Regex pattern → deduplicates emails     │
│                                                         │
│  3. send_email_with_resume()  [loop]                    │
│     └─ Builds MIMEMultipart email (HTML body)          │
│     └─ Attaches PDF resume                             │
│     └─ Connects to smtp.gmail.com:587 via TLS          │
│     └─ Sends → waits 30s → repeats for next email      │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 Challenges Faced & Learnings

| Challenge | Solution & Learning |
|---|---|
| **LinkedIn's dynamic content loading** | Used `WebDriverWait` with `ExpectedConditions` instead of raw `time.sleep()` for reliable element detection |
| **Stale email data / duplicates** | Wrapped extracted emails in `set()` before returning to deduplicate efficiently |
| **Gmail SMTP authentication** | Learned that standard passwords don't work with SMTP — discovered Google App Passwords as the secure workaround |
| **Chrome blocking automation detection** | Used `maximize_window()` and added human-like scroll delays to reduce bot detection risk |
| **File path errors on Windows** | Used raw strings (`r"path\to\file"`) to handle backslashes in Windows file paths |
| **Email body rendering** | Used `MIMEText` with `html` subtype instead of `plain` for professional formatting with bold text and styling |

---


## 👨‍💻 Author

<div align="center">

### Harikishor Sahu

**B.S. Student @ IIT Patna**
*Focused on Full-Stack Development & Data Science*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sahuharikishor)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/harikishor-sahu-25ba1a281/)


</div>

---
## ⚠️ Disclaimer

> This script is for **educational purposes only**.
> Web scraping and automation bots violate [LinkedIn's Terms of Service](https://www.linkedin.com/legal/user-agreement).
> Use this tool responsibly, add sufficient delays (`time.sleep`), and **do not spam recruiters**.
> I am not responsible for any account bans, restrictions, or legal consequences arising from misuse of this tool.

---

<div align="center">

⭐ **If this project helped you land a job, drop a star!** ⭐

*Built with ☕ and Python at IIT Patna*

</div>