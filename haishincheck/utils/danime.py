import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def danime_scraping(driver, title):
    try:
        input_title = title_convert(title)

        url = "https://anime.dmkt-sp.jp/animestore/CF/search_index"
        driver.get(url)
        time.sleep(3)

        search_box = driver.find_element(By.CSS_SELECTOR, '#searchKey')
        search_box.clear()
        search_box.send_keys(title)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div.btnSearch > a > i.icon').click()
        time.sleep(3)

        searched_title_tags = driver.find_elements(By.CSS_SELECTOR, 'div.itemModule')
        page_url = driver.current_url

        for searched_title_tag in searched_title_tags:
            searched_title = searched_title_tag.find_element(By.CSS_SELECTOR, 'h3.line2').text
            cleaned_searched_title = title_convert(searched_title)
            
            if input_title in cleaned_searched_title:
                try:
                    is_rental = searched_title_tag.find_element(By.CSS_SELECTOR, 'section > ul.option > li')
                    if is_rental:
                        result = 'レンタル'
                except:
                    result = '見放題'
                
                break

        else:
            result = 'なし'

    except:
        result = '取得失敗'


    driver.quit()
    return result, page_url


