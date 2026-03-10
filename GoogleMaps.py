from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

# KEYWORDS TO SEARCH
keywords = [
"restaurants in Faisalabad Pakistan",
"cafes in Faisalabad Pakistan",
"coffee shops in Faisalabad Pakistan",
"fast food in Faisalabad Pakistan",
"bbq restaurants in Faisalabad Pakistan",
"pizza in Faisalabad Pakistan",
"burger shops in Faisalabad Pakistan",
"shawarma in Faisalabad Pakistan",
"biryani restaurants in Faisalabad Pakistan",
"dessert shops in Faisalabad Pakistan",
"tea stalls in Faisalabad Pakistan",
"ice cream shops in Faisalabad Pakistan",
"hotels in Faisalabad Pakistan",
"guest houses in Faisalabad Pakistan"
]

all_data = []
seen_places = set()

for keyword in keywords:

    print("Searching:", keyword)

    search_url = "https://www.google.com/maps/search/" + keyword.replace(" ", "+")
    driver.get(search_url)

    time.sleep(5)

    try:
        feed = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )
    except:
        continue

    # SCROLL RESULTS (increase for more businesses)
    for i in range(30):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", feed
        )
        time.sleep(2)

    places = driver.find_elements(By.XPATH, '//a[contains(@href,"/maps/place")]')

    print("Places found:", len(places))

    for place in places:

        try:
            place.click()
            time.sleep(3)

            try:
                name = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//h1[contains(@class,"DUwDvf")]')
                    )
                ).text
            except:
                name = ""

            # skip duplicates
            if name in seen_places:
                continue

            seen_places.add(name)

            try:
                address = driver.find_element(
                    By.XPATH, '//button[@data-item-id="address"]'
                ).text.replace("\ue0c8", "")
            except:
                address = ""

            try:
                rating = driver.find_element(
                    By.XPATH, '//div[@role="img"]'
                ).get_attribute("aria-label")
            except:
                rating = ""

            latitude = ""
            longitude = ""

            url = driver.current_url

            if "@" in url:
                coords = url.split("@")[1].split(",")
                latitude = coords[0]
                longitude = coords[1]

            business = {
                "name": name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "rating": rating
            }

            all_data.append(business)

            print("Collected:", name)

        except:
            pass


with open("faisalabad_food_businesses.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)

print("Total businesses scraped:", len(all_data))

driver.quit()