import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def paravi_scraping(driver, title):
    try:
        input_title = title_convert(title)
        
        page_url = f'https://www.paravi.jp/search?q={title}'
        driver.get(page_url)
        time.sleep(4)


        # 検索でヒットした上位10件を取得
        works = driver.find_elements(By.CSS_SELECTOR, 'div.slider-item')[:10]

        # 検索したタイトルと一致するものを取得(予告版は排除)
        for work in works:
            work_title = work.find_element(By.CSS_SELECTOR, 'h3.title-card-title').text
            cleaned_searched_title = title_convert(work_title)
            if (input_title in cleaned_searched_title) and ('【無料・予告】' not in work_title) and ('【予告】' not in work_title):
                work.click()
                time.sleep(3)
 
                driver.find_elements(By.CSS_SELECTOR, 'div.watch-info')
                driver.find_elements(By.CSS_SELECTOR, 'div.title-overview-content')

                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                # ページ構成が2パターンある
                page_type1 = soup.select_one('div.watch-info')
                page_type2 = soup.select_one('div.title-overview-content')

                if page_type1:
                    tag = page_type1.select_one('div.tag-list')
                    if tag is None:
                        result = '見放題'
                    elif 'レンタル' in tag.text:
                        result = 'レンタル'
                    else:
                        result = '見放題'
                    break

                elif page_type2:
                    tag = page_type2.select_one('div.tag-list')
                    if tag is None:
                        result = '見放題'
                    elif 'レンタル' in tag.text:
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
