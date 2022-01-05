import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def danime_scraping(driver, title):
    try:
        true_flag = False
        input_title = title_convert(title)

        url = "https://anime.dmkt-sp.jp/animestore/CF/search_index"
        driver.get(url)
        time.sleep(4)

        search_box = driver.find_element(By.CSS_SELECTOR, '#searchKey')
        search_box.clear()
        search_box.send_keys(title)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'div.btnSearch > a > i.icon').click()
        time.sleep(3)

        searched_title_tags = driver.find_elements(By.CSS_SELECTOR, 'div.itemModule')

        for searched_title_tag in searched_title_tags:
            searched_title = searched_title_tag.find_element(By.CSS_SELECTOR, 'h3.line2').text

            cleaned_searched_title = title_convert(searched_title)
            title_length = len(input_title)

            if title_length <= 7:
                # 完全一致しているか
                if input_title in cleaned_searched_title:
                    true_flag = True

            else:
                # 70％以上一致しているか
                title_length_70percent = int(round(title_length * 0.7, 0))
                for initial, last in enumerate(range(title_length_70percent, title_length+1)):
                    confirmed_title = input_title[initial:last]
                    if confirmed_title in cleaned_searched_title:
                        true_flag = True
                        break

            if true_flag:
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
        result = 'エラー'


    return result


