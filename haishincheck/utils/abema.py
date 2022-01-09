import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def abema_scraping(driver, title):
    try:
        input_title = title_convert(title)
        
        # page_url = f"https://abema.tv/search?q={title}"
        page_url = f"https://abema.tv/"
        driver.get(page_url)
        time.sleep(5)
        # driver.find_elements(By.CSS_SELECTOR, 'li.com-search-SearchResultsVideoSection__list-item')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        searchResultsVideoList = soup.select('li.com-search-SearchResultsVideoSection__list-item')

        for searchResult in searchResultsVideoList:
            work_title = searchResult.select_one('p.com-search-SearchSeriesListItem__heading > span').text
            cleaned_searched_title = title_convert(work_title)

            if (input_title in cleaned_searched_title):
                rental_icon = searchResult.select_one('div.com-m-Thumbnail__coin-icon')
                if rental_icon:
                    result = 'レンタル'
                else:
                    result = '見放題'
                break
        
        else:
            result = 'なし'

    except:
        result = '取得失敗'

    html = str(html)
    driver.quit()
    return result, page_url, html
