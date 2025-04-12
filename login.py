import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
import time

# Read environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_PHONE = os.getenv('TWILIO_FROM_PHONE')
TWILIO_TO_PHONE = os.getenv('TWILIO_TO_PHONE')

# Set up headless Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')  # For environments like GitHub Actions
options.add_argument('--disable-dev-shm-usage')  # To prevent issues with resource usage

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get("https://control.dejero.com/users/sign_in")

# Wait for the page to load
time.sleep(5)

# Perform login
username = driver.find_element(By.ID, "user_email")
username.send_keys("PLACEHOLDER_EMAIL")

password = driver.find_element(By.ID, "user_password")
password.send_keys("PLACEHOLDER_PASSWORD")

driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
time.sleep(5)

# Check if login was successful
if "Sign in" not in driver.page_source:
    print("Login successful")
else:
    print("Login failed")

# Navigate to the desired page
try:
    driver.implicitly_wait(20)
    link = driver.find_element(By.LINK_TEXT, "5261644 - CPC Engo")
    link.click()
except Exception as e:
    print(f"Elemtent disappeared")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_FROM_PHONE,
        body='The stream is down!',
        to=TWILIO_TO_PHONE
    )
    print(message.sid)
    driver.quit()
    exit()  

# Extract numeric value
def get_numeric_value(driver):
    try:

        el = driver.find_element(By.XPATH, "(//div[@class='data-property'])[8]")    
        text = el.text.strip().replace(',','')
        print(f"Extracted text: '{text}'")  # Debugging line

        return int(text)
    except NoSuchElementException:
        print(f"Elemtent disappeared")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=TWILIO_FROM_PHONE,
            body='The stream is down!',
            to=TWILIO_TO_PHONE
        )
        print(message.sid)
        driver.quit()
        exit()
        
# Check if value is less than 2000
time.sleep(10)  # Wait for the page to load
if get_numeric_value(driver) < 2000:
    # Send an SMS if the numeric value is below 1000
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_FROM_PHONE,
        body='Your throughput has dropped below 2 mb!',
        to=TWILIO_TO_PHONE
    )
    print(message.sid)

# Close the browser
driver.quit()