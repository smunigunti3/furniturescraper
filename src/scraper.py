from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
<<<<<<< Updated upstream
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
=======
from selenium.webdriver import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.ikea.com/us/en/cat/sofas-sectionals-fu003/")
time.sleep(3)

while True:
    try:
        cookie_notification = driver.find_element(By.ID,"onetrust-accept-btn-handler")
        if cookie_notification.is_displayed():
            cookie_notification.click()
        show_more_button = driver.find_element(By.CLASS_NAME, "plp-btn--secondary")
        ActionChains(driver).click(show_more_button).perform()
        print("Show more button clicked")
        time.sleep(3)
    except:
        print("No more pages")
        break

product_element_list = driver.find_elements(By.CLASS_NAME, "plp-fragment-wrapper")

results = []
for element in product_element_list:
    name = element.find_element(By.CLASS_NAME, "plp-mastercard")
    results.append(name)

results2 = []
for element in results:
    name = element.find_element(By.CLASS_NAME, "plp-mastercard__image")
    results2.append(name)

productlist = []
for element in results2:
    product_element = element.find_element(By.TAG_NAME,'a')
    product = product_element.get_attribute('href')
    productlist.append(product)

# for product in productlist:
#     print(product)

driver.quit()
>>>>>>> Stashed changes
