import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def ckunkin_scraping(driver, title):
    try:
        input_title = title_convert(title)
        
        page_url = f"https://video.crank-in.net/search?type=0&limit=500&free_filter=0&sort=0&word={title}"
        driver.get(page_url)
        time.sleep(4)
        driver.find_elements(By.CSS_SELECTOR, 'ul.panel > li')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('ul.panel > li')[:10]

        for work in works:
            work_title = work.select_one('a > img').get('alt')
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