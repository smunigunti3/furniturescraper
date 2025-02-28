from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Visit the URL
url = "https://megafurniture.us/collections/sofas"
driver.get(url)

# Give the page a little time to load
time.sleep(3)

try:
    # Find all product names using the 'card__title' class
    product_elements = driver.find_elements(By.CLASS_NAME, "card__title")

    # Print out each product name
    for product in product_elements:
        print(product.text)

except Exception as e:
    print("Error occurred:", e)

finally:
    driver.quit()
