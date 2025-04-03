import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
import json

def find_furniture_urls():
    driver = webdriver.Chrome()
    driver.get("https://www.ikea.com/us/en/cat/products-products/")
    time.sleep(3)

    furniture_selection_urls = driver.find_elements(By.CLASS_NAME, "vn-link")
    furniture_urls = set()
    for url in furniture_selection_urls:
        class_attribute = url.get_attribute('class')
        link_text = url.text.strip()
        class_to_skip = 'vn-accordion__image'
        text_to_skip = 'Shop all'
        if class_to_skip in class_attribute or link_text == text_to_skip:
            continue
        furniture_url = url.get_attribute('href')
        furniture_urls.add(furniture_url)

    csv_filename = 'furniture_links.csv'
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Furniture Links"])  # Header
        for link in furniture_urls:
            writer.writerow([link])

    driver.quit()
    return furniture_urls


def webpage_scraper(section_url: str):
    driver = webdriver.Chrome()
    driver.get(section_url)
    time.sleep(1)
    while True:
        try:
            cookie_notification = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            if cookie_notification.is_displayed():
                cookie_notification.click()
            show_more_button = driver.find_element(By.CLASS_NAME, "plp-btn--secondary")
            ActionChains(driver).click(show_more_button).perform()
            time.sleep(1)
        except:
            break

    product_element_list = driver.find_elements(By.CLASS_NAME, "plp-fragment-wrapper")

    results = []
    for element in product_element_list:
        name = element.find_element(By.CLASS_NAME, "plp-mastercard")
        results.append(name)

    results2 = []
    for element in results:
        try:
            name = element.find_element(By.CLASS_NAME, "plp-mastercard__image")
            results2.append(name)
        except:
            continue

    productlist = set()
    for element in results2:
        product_element = element.find_element(By.TAG_NAME, 'a')
        product = product_element.get_attribute('href')
        productlist.add(product)

    driver.quit()
    return productlist

def extract_product_details(product_url):
    driver = webdriver.Chrome()
    driver.get(product_url)
    time.sleep(1)

    product_div = driver.find_element(By.CLASS_NAME, "pip-product__subgrid")

    product_id = product_div.get_attribute('data-product-id') or "N/A"
    product_type = product_div.get_attribute('data-product-type') or "N/A"
    product_name = product_div.get_attribute('data-product-name') or "N/A"
    product_rating = product_div.get_attribute('data-product-rating') or "N/A"
    product_price = product_div.get_attribute('data-product-price') or "N/A"

    #Can also add measurement data

    hydration_props = product_div.get_attribute("data-hydration-props")
    if hydration_props:
        try:
            hydration_data = json.loads(hydration_props)
            product_description = hydration_data.get("productSummary", {}).get("description", "N/A")
        except json.JSONDecodeError:
            product_description = "N/A"
    else:
        product_description = "N/A"

    driver.quit()

    return{
        "Product URL": product_url,
        "Product ID": product_id,
        "Product Type": product_type,
        "Product Name": product_name,
        "Product Rating": product_rating,
        "Product Price": product_price,
        "Product Description": product_description,
    }


'''

# CODE TO BE RUN - UNCOMMENT AS NECESSARY

# TO FIND THE FURNITURE SECTION URLS AND PUT THEM INTO furniture_links.csv
find_furniture_urls()

# TO EXTRACT THE PRODUCT PAGE URLS AND PUT THEM INTO ikea_product_urls.csv
section_urls = []
with open('furniture_links.csv', mode="r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        section_urls.append(row[0])

all_products = []
for section_url in section_urls:
    product_urls = webpage_scraper(section_url)
    for product_url in product_urls:
        all_products.append({"Product URL": product_url})

csv_filename = 'ikea_product_urls.csv'
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Product URL"])
    writer.writeheader()
    writer.writerows(all_products)


# TO EXTRACT THE INDIVIDUAL PRODUCT FEATURES AND PUT THEM INTO ikea_full_product_data.csv
product_urls = []
with open('ikea_product_urls.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_urls.append(row["Product URL"])

all_product_data = []
for url in product_urls[:5]:
    product_data = extract_product_details(url)
    if product_data:
        all_product_data.append(product_data)

csv_filename = 'ikea_full_product_data.csv'
with open(csv_filename, mode="w", newline="") as file:
    fieldnames = ["Product URL", "Product ID", "Product Type", "Product Name",
                  "Product Rating", "Product Price", "Product Description"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_product_data)

'''




