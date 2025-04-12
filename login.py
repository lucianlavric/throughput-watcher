import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
import requests
import time


# Read and validate environment variables
required_env_vars = {
    "TWILIO_ACCOUNT_SID": os.getenv('TWILIO_ACCOUNT_SID'),
    "TWILIO_AUTH_TOKEN": os.getenv('TWILIO_AUTH_TOKEN'),
    "TWILIO_FROM_PHONE": os.getenv('TWILIO_FROM_PHONE'),
    "TWILIO_TO_PHONE": os.getenv('TWILIO_TO_PHONE'),
    "USER_EMAIL": os.getenv('USER_EMAIL'),
    "USER_PASSWORD": os.getenv('USER_PASSWORD'),
    "GITHUB_REPOSITORY": os.getenv('GITHUB_REPOSITORY'),
    "GITHUB_TOKEN": os.getenv('GITHUB_TOKEN'),
}

# Validate that all required environment variables are set
for var_name, var_value in required_env_vars.items():
    if not var_value:
        raise EnvironmentError(f"Error: The environment variable '{var_name}' is not set.")

# Use the validated environment variables throughout the script
TWILIO_ACCOUNT_SID = required_env_vars["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = required_env_vars["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_PHONE = required_env_vars["TWILIO_FROM_PHONE"]
TWILIO_TO_PHONE = required_env_vars["TWILIO_TO_PHONE"]
USER_EMAIL = required_env_vars["USER_EMAIL"]
USER_PASSWORD = required_env_vars["USER_PASSWORD"]
GITHUB_REPOSITORY = required_env_vars["GITHUB_REPOSITORY"]
GITHUB_TOKEN = required_env_vars["GITHUB_TOKEN"]

def handle_element_disappearance():
    print("Element disappeared")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_FROM_PHONE,
        body='The stream is down!',
        to=TWILIO_TO_PHONE
    )
    print(message.sid)
    cancel_workflow()
    driver.quit()
    exit()


# Set up headless Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')  # For environments like GitHub Actions
options.add_argument('--disable-dev-shm-usage')  # To prevent issues with resource usage

# Initialize the driver
driver = webdriver.Chrome(options=options)

try:
    # Open the URL
    driver.get("https://control.dejero.com/users/sign_in")

    # Wait for the page to load
    time.sleep(5)

    # Perform login
    username = driver.find_element(By.ID, "user_email")
    username.send_keys("USER_EMAIL")

    password = driver.find_element(By.ID, "user_password")
    password.send_keys("USER_PASSWORD")

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(5)

    def cancel_workflow():
        # GitHub repository details
        repo = os.getenv('GITHUB_REPOSITORY')  # e.g., "username/repo-name"
        token = os.getenv('GITHUB_TOKEN')  # GitHub token provided by the workflow

        # Get the current workflow run ID
        runs_url = f"https://api.github.com/repos/{repo}/actions/runs"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(runs_url, headers=headers)
        
        if response.status_code == 200:
            runs = response.json()
            if "workflow_runs" in runs and len(runs["workflow_runs"]) > 0:
                run_id = runs["workflow_runs"][0]["id"]  # Get the latest run ID
                
                # Cancel the workflow run
                cancel_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/cancel"
                cancel_response = requests.post(cancel_url, headers=headers)
                
                if cancel_response.status_code == 202:
                    print("Workflow run canceled successfully.")
                else:
                    print(f"Failed to cancel workflow: {cancel_response.status_code}, {cancel_response.text}")
            else:
                print("No workflow runs found.")
        else:
            print(f"Failed to fetch workflow runs: {response.status_code}, {response.text}")


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
        handle_element_disappearance()


    # Extract numeric value
    def get_numeric_value(driver):
        try:

            el = driver.find_element(By.XPATH, "(//div[@class='data-property'])[8]")    
            text = el.text.strip().replace(',','')
            print(f"Extracted text: '{text}'")  # Debugging line

            return int(text)
        except NoSuchElementException:
            handle_element_disappearance()
            
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
finally:
    driver.quit()