from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Setup Chrome Options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Load environment variables
load_dotenv()
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RESUME_FILE_PATH = os.getenv("RESUME_PATH")

def login_to_linkedin():
    try:
        print("Starting the browser...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(driver, 15)   
        
        print("Waiting for login fields...")
        
        try:
            username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = driver.find_element(By.ID, "password")
        except:
            print("Trying alternative login IDs...")
            username_field = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
            password_field = driver.find_element(By.ID, "session_password")
        
        print("Entering credentials...")
        username_field.send_keys(LINKEDIN_USERNAME)
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        
        time.sleep(5) 
        
        # Check if login was actually successful or if Captcha appeared
        if "login" in driver.current_url.lower() or "checkpoint" in driver.current_url.lower():
            print("Captcha or Security Check detected!")
            print("Please solve the puzzle manually in the Chrome window. You have 30 seconds...")
            time.sleep(30)
            
        print("Successfully logged in!")
        return driver

    except Exception as e:
        print(f"Login failed: {e}")
        if 'driver' in locals():
            driver.quit()
        return None
    
def search_jobs_and_extract_emails(driver):
    query = 'python developer "email me" OR "drop your resume"'
    search_url = f"https://www.linkedin.com/search/results/content/?keywords={query}"
    
    print(f"Navigating to LinkedIn Posts search for: {query}")
    driver.get(search_url)
    time.sleep(15)  

    # Click "see more" buttons to expand posts
    print("Expanding all posts...")
    try:
        see_more_buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"see more") or contains(text(),"See more")]')
        for btn in see_more_buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
            except:
                pass
        print(f"Clicked {len(see_more_buttons)} 'see more' buttons")
    except:
        print("No see more buttons found")

    # Scroll slowly like a human
    print("Scrolling slowly to load more data...")
    for _ in range(10):  
        driver.execute_script("window.scrollBy(0, 500);")  
        time.sleep(2)

    page_text = driver.find_element(By.TAG_NAME, "body").text
    
    print("Hunting for email addresses using Regex...")
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    emails = list(set(re.findall(email_pattern, page_text)))

    # Filter out LinkedIn's own system emails
    emails = [e for e in emails if "linkedin.com" not in e and "sentry.io" not in e]

    if emails:
        print(f"Success! Found {len(emails)} emails: {emails}")
    else:
        print("No emails found. LinkedIn might be blocking text or posts have no emails.")
    
    return emails

def send_email_with_resume(receiver_email):
    print(f"Preparing to send email to: {receiver_email}")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Application for Software Developer Role"

    html_body = """
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi Hiring Manager,</p>
        <p>I came across your recent post on LinkedIn regarding the <b>Software Developer</b> position.</p>
        <p>I have solid experience in backend development and would love to be considered for this role.</p>
        <p>Please find my resume attached to this email. Looking forward to your response.</p>
        <br>
        <p>Best Regards,<br>
        <b>Harikishor Sahu</b></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with open(RESUME_FILE_PATH, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(RESUME_FILE_PATH))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(RESUME_FILE_PATH)}"'
            msg.attach(part)
            print("Resume attached successfully.")
    except Exception as e:
        print(f"Error attaching resume: {e}. Email will NOT be sent.")
        return False

    try:
        print("Connecting to Gmail server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(SENDER_EMAIL, APP_PASSWORD)
        print("Sending email...")
        server.send_message(msg)
        server.quit() 
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    driver = login_to_linkedin()
    
    if driver:
        extracted_emails = search_jobs_and_extract_emails(driver)

        print("\nClosing browser. Moving to Email phase...")
        driver.quit()
        
        if extracted_emails:
            print("\n" + "="*40)
            print("SENDING JOB APPLICATIONS")
            print("="*40)
            
            for email_id in extracted_emails:
                send_email_with_resume(email_id)
                time.sleep(30) 
                
            print("\nAll applications sent successfully!")
        else:
            print("\nTask ended: No emails found.")
    else:
        print("Stopping script because login failed.")