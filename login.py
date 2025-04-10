from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException
from twilio.rest import Client
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
TWILIO_TO_PHONE = os.getenv("TWILIO_TO_PHONE")


if __name__ == "__main__":

    options = uc.ChromeOptions()

    options.headless = False

    driver = uc.Chrome(
        use_subprocess = False,
        options = options,
    )

    driver.get("https://control.dejero.com/users/sign_in")

    time.sleep(5)

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

    link = driver.find_element(By.LINK_TEXT, "5261644 - CPC Engo")
    link.click()

    def get_numeric_value(driver):
        el = driver.find_element(By.CLASS_NAME, "data-property")
        text = el.text.strip().replace(',', '')
        return int(text)

    # Instead of a long wait, just do a short wait to ensure the element is loaded
    short_wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)
    short_wait.until(lambda d: d.find_element(By.CLASS_NAME, "data-property"))

    value = get_numeric_value(driver)
    print(f"Current value: {value}")

    if value < 1000:
        # Send Twilio message
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=TWILIO_FROM_PHONE,
            body='Your throughput has dropped below 1 mb!',
            to=TWILIO_TO_PHONE
        )
        print("🚨 Alert sent!", message.sid)
    else:
        print("Value is above threshold. No alert sent.")

driver.quit()