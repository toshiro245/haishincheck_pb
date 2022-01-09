import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def hulu_scraping(driver, title):
    try:
        result = 'なし'
        input_title = title_convert(title)

        url = f'https://www.hulu.jp/search?q={title}'
        driver.get(url)
        time.sleep(4)

        search_works_free = driver.find_elements(By.CSS_SELECTOR, "div.gallery-content div.slider-item > div.title-card > div.sliderRefocus")[:10]
        search_works_rental = driver.find_elements(By.CSS_SELECTOR, "div.canvas-row div.slider-item > div.title-card > div.sliderRefocus")[:10]

        for search_work_free in search_works_free:
            work_title = search_work_free.get_attribute('aria-label')
            cleaned_searched_title = title_convert(work_title)
            if input_title in cleaned_searched_title:
                result = '見放題'


        for search_work_rental in search_works_rental:
            work_title = search_work_rental.get_attribute('aria-label')
            cleaned_searched_title = title_convert(work_title)
            if input_title in cleaned_searched_title:
                result = 'レンタル'

    except:
        result = '取得失敗'


    driver.quit()
    return result, url


