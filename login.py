from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException
from twilio.rest import Client



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
        text = el.text.strip().replace(',', '')  # remove commas if the number is like "1,234"
        return int(text)

    try:
        wait = WebDriverWait(driver, timeout=7200, poll_frequency=1)  # Wait up to 2 hours, check every second

        wait.until(lambda driver: get_numeric_value(driver) < 1000)

        account_sid = 'PLACEHOLDER_TWILIO_ACCOUNT_SID'
        auth_token = 'PLACEHOLDER_TWILIO_TOKEN'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+17855724926',
            body='Your throughput has dropped below 1 mb!',
            to='+15195006509'
        )
        print(message.sid)

        WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID,"ctl00_ContentPlaceHolder1_..."), "The text you want"))

    except TimeoutException:
        print("Timed out waiting for a drop")

driver.quit()