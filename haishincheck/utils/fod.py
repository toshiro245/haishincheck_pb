import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert



def fod_scraping(driver, title):
    try:

        input_title = title_convert(title)

        url = f'https://fod.fujitv.co.jp/psearch?keyword={title}'
        driver.get(url)
        time.sleep(4)

        work_wrapper = driver.find_element(By.XPATH, '//section[h1[text()="検索結果"]]')
        works = work_wrapper.find_elements(By.CSS_SELECTOR, 'li.sw-Lineup_Item')

        work_url_list = []
        work_title_list = []

        for work in works:
            work_url = work.find_element(By.CSS_SELECTOR, 'div.sw-Lineup > a').get_attribute('href')
            work_title = work.find_element(By.CSS_SELECTOR, 'h3.sw-Lineup_Title').text
            work_url_list.append(work_url)
            work_title_list.append(work_title)


        for work_url, work_title in zip(work_url_list, work_title_list):
            
            cleaned_searched_title = title_convert(work_title)
            
            if input_title in cleaned_searched_title:
                driver.get(work_url)
                time.sleep(4)

                html = driver.page_source
                detail_soup = BeautifulSoup(html, 'lxml')

                is_rental = detail_soup.select_one('div.geGePr-Status > div.geGePr-Tags')
                if is_rental:
                    if 'レンタル' in is_rental.text:
                        result = 'レンタル'
                    else:
                        result = '見放題'
                
                else:
                    result = '見放題'

                break


        else:
            result = 'なし'
    
    except:
        result = '取得失敗'


    driver.quit()
    return result, url

