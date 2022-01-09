import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def dtv_scraping(driver, title):
    try:
        input_title = title_convert(title)
        modified_title = title.replace('%', 'パーセント').replace('％', 'パーセント')
        
        page_url = f"https://video.dmkt-sp.jp/search/?q={modified_title}"
        driver.get(page_url)
        time.sleep(4)

        driver.find_elements(By.CSS_SELECTOR, 'li.dup-card-list-grid-max6col-m__item--TmiMC')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        searchResultsVideoList = soup.select('li.dup-card-list-grid-max6col-m__item--TmiMC')
        for searchResultsVideo in searchResultsVideoList:
            work_title = searchResultsVideo.select_one('h3.dup-text-ellipsis-default-m__root--1toBF').text
            cleaned_searched_title = title_convert(work_title)

            if (input_title in cleaned_searched_title):
                is_rental = searchResultsVideo.select_one('div.dup-card-grid-item-default-m__rental--1GrDL')
                if is_rental:
                    result = 'レンタル'
                else:
                    result = '見放題'
                break

        else:
            result = 'なし'


    except:
        result = '取得失敗'


    driver.quit()
    return result, page_url
