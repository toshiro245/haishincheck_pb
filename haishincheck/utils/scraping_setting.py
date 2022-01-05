from time import sleep
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager



def driver_setting():
    driver_path = '/app/.chromedriver/bin/chromedriver'
    # driver_path = '/Users/ToshiroTasaka/PythonPractice_VSCODE/20211221_HaishinCheck/tools/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        executable_path=driver_path,
        # ChromeDriverManager().install(),
        options=options
    )
    driver.implicitly_wait(5)
    return driver



# def driver_quit(driver):
    # sleep(2)
    # driver.quit()