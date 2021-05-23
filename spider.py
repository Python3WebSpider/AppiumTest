import json
import os
from spider import main
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from loguru import logger


SERVER = 'http://localhost:4723/wd/hub'

DESIRED_CAPABILITIES = {
    "platformName": "Android",
    "deviceName": "SM_G9860",
    "appPackage": "com.goldze.mvvmhabit",
    "appActivity": ".ui.MainActivity",
    "noReset": True
}
PACKAGE_NAME = DESIRED_CAPABILITIES['appPackage']
TOTAL_NUMBER = 100


driver = webdriver.Remote(SERVER, DESIRED_CAPABILITIES)
wait = WebDriverWait(driver, 30)
window_size = driver.get_window_size()
window_width, window_height = window_size.get(
    'width'), window_size.get('height')


def scrape_detail(element):
    logger.debug(f'scraping {element}')
    element.click()
    wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/detail')))
    title = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/title'))).get_attribute('text')
    categories = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/categories_value'))).get_attribute('text')
    score = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/score_value'))).get_attribute('text')
    minute = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/minute_value'))).get_attribute('text')
    published_at = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/published_at_value'))).get_attribute('text')
    drama = wait.until(EC.presence_of_element_located(
        (By.ID, f'{PACKAGE_NAME}:id/drama_value'))).get_attribute('text')
    driver.back()
    return {
        'title': title,
        'categories': categories,
        'score': score,
        'minute': minute,
        'published_at': published_at,
        'drama': drama
    }


def scrape_index():
    items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, f'//android.widget.LinearLayout[@resource-id="{PACKAGE_NAME}:id/item"]')))
    return items


scraped_titles = []


OUTPUT_FOLDER = 'movie'
os.path.exists(OUTPUT_FOLDER) or os.makedirs(OUTPUT_FOLDER)


def save_data(element_data):
    with open(f'{OUTPUT_FOLDER}/{element_data.get("title")}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(element_data, ensure_ascii=False, indent=2))
        logger.debug(f'saved as file {element_data.get("title")}.json')


def get_element_title(element):
    try:
        element_title = element.find_element_by_id(
            f'{PACKAGE_NAME}:id/tv_title').get_attribute('text')
        return element_title
    except NoSuchElementException:
        return None


def scroll_up():
    driver.swipe(window_width * 0.5, window_height * 0.8,
                 window_width * 0.5, window_height * 0.5, 1000)


def main():
    while len(scraped_titles) < TOTAL_NUMBER:
        elements = scrape_index()
        for element in elements:
            element_title = get_element_title(element)
            if not element_title or element_title in scraped_titles:
                continue
            element_location = element.location
            element_y = element_location.get('y')
            if element_y / window_height > 0.8:
                logger.debug(f'scroll up')
                scroll_up()
            element_data = scrape_detail(element)
            scraped_titles.append(element_title)
            logger.debug(f'scraped data {element_data}')
            save_data(element_data)


if __name__ == '__main__':
    main()
