import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def musicjp_scraping(driver, title):
    try:
        input_title = title_convert(title)
        
        page_url = f"https://music-book.jp/video/search/title?keyword={title}"
        driver.get(page_url)
        time.sleep(4)
        driver.find_elements(By.CSS_SELECTOR, 'div.image-list-item')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('div.image-list-item')

        for work in works:
            work_title = work.select_one('p.title').text
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
