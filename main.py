from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

server = 'http://localhost:4723/wd/hub'

desired_capabilities = {
    "platformName": "Android",
    "deviceName": "SM_G9860",
    "appPackage": "com.goldze.mvvmhabit",
    "appActivity": ".ui.MainActivity",
    "noReset": True
}

driver = webdriver.Remote(server, desired_capabilities)
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout')))
window_size = driver.get_window_size()
width, height = window_size.get('width'), window_size.get('height')
driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.2, 1000)
