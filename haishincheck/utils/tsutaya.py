import time
import urllib.parse
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def tsutaya_scraping(driver, title):
    try:
        input_title = title_convert(title)
        encode_title = urllib.parse.quote(title, encoding='shift-jis')
        
        page_url = f'https://movie-tsutaya.tsite.jp/netdvd/dvd/searchDvdHmo.do?k={encode_title}'
        driver.get(page_url)
        time.sleep(5)
        driver.find_elements(By.CSS_SELECTOR, '#container-product-search > div.card-box-searchdvd')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('#container-product-search > div.card-box-searchdvd')

        for work in works:
            work_title = work.select_one('div.card-body-searchdvd > a').text
            cleaned_searched_title = title_convert(work_title)
            if (input_title in cleaned_searched_title):
                result = 'レンタル'
                break

        else:
            result = 'なし'
    

    except:
        result = '取得失敗'
    

    driver.quit()
    return result, page_url
