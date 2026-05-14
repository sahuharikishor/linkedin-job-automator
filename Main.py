from selenium import webdriver
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


# LinkedIn account details 

load_dotenv()
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin():
    try:
        print("Starting the browser...")
        driver = webdriver.Chrome()
        driver.maximize_window()
        
        driver.get("https://www.linkedin.com/login")
        
        wait = WebDriverWait(driver, 15)   
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        
        print("Entering credentials...")
        username_field.send_keys(LINKEDIN_USERNAME)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        
        time.sleep(5) 
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

    print("Scrolling to load more data...")
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    page_text = driver.find_element(By.TAG_NAME, "body").text
    
    print("Hunting for email addresses using Regex...")
    email_pattern = r'[a-zA-Z0-9.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    emails = list(set(re.findall(email_pattern, page_text))) 

    if emails:
        print(f"Success! Found {len(emails)} emails: {emails}")
    else:
        print("No emails found. LinkedIn might be blocking text or posts have no emails.")
    
    return emails


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RESUME_FILE_PATH = os.getenv("RESUME_PATH")

def send_email_with_resume(receiver_email):
    print(f"Preparing to send email to: {receiver_email}")
    
    # email container (MIMEMultipart)
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Application for Software Developer Role"

    # email body
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

    # Attach the Resume
    try:
        with open(RESUME_FILE_PATH, "rb") as file:
            # Read the PDF file and attach it
            part = MIMEApplication(file.read(), Name=os.path.basename(RESUME_FILE_PATH))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(RESUME_FILE_PATH)}"'
            msg.attach(part)
            print("Resume attached successfully.")
    except FileNotFoundError:
        print(f"Error: Could not find the file '{RESUME_FILE_PATH}'. Email will NOT be sent.")
        return False

    # Connect to Gmail's SMTP server and send the email
    try:
        print("Connecting to Gmail server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        
        print("Logging in to Gmail...")
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        print("Sending email...")
        server.send_message(msg)
        
        server.quit() # Close the connection
        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Entry point of the script
if __name__ == "__main__":
    
    # Login to LinkedIn
    driver = login_to_linkedin()
    
    if driver:
        # Search and Extract Emails
        extracted_emails = search_jobs_and_extract_emails(driver)

        print("\n Closing browser. Moving to Email phase...")
        driver.quit()
        
        # Send Emails
        if extracted_emails:
            print("\n" + "="*40)
            print("SENDING JOB APPLICATIONS")
            print("="*40)
            
            for email_id in extracted_emails:
                send_email_with_resume(email_id)
                time.sleep(30) 
                
            print("\n All applications sent successfully!")
        else:
            print("\n Task ended: No emails found.")


