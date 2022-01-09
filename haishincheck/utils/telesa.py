import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def telesa_scraping(driver, title):
    try:
        true_flag = False
        input_title = title_convert(title)
        
        page_url = f'https://www.telasa.jp/search?q={title}'
        driver.get(page_url)
        time.sleep(4)
        driver.find_elements(By.CSS_SELECTOR, 'section.vdcarousel')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # 検索ヒットした作品を全件取得
        works_blocks = soup.select('section.vdcarousel')

        for works_block in works_blocks:
            # カテゴリ(レンタルか見放題か)
            result = works_block.select_one('div.carousel-header > span.title').text
            if result == 'PPV':
                result = 'レンタル'
            elif result == 'Unlimited':
                result = '見放題'

            works = works_block.select('div.carousel-container div.kks-slider__item > a')
            for work in works:
                work_title = work.select_one('div.vdcard__content > div.vdcard__name ').text
                cleaned_searched_title = title_convert(work_title)
                if (input_title in cleaned_searched_title):
                    true_flag = True
                
                if true_flag:
                    break

            if true_flag:
                break


        else:
            result = 'なし'
    
    except:
        result = '取得失敗'


    driver.quit()
    return result, page_url
