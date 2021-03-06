import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def amazon_scraping(driver, title):
    try:
        input_title = title_convert(title)

        url = f"https://www.amazon.co.jp/s?k={title}&i=instant-video"
        driver.get(url)
        time.sleep(4)
        driver.find_elements(By.CSS_SELECTOR, 'div.s-result-item > div.sg-col-inner')

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        #検索結果タイトルを取得
        searched_works = soup.select('div.s-result-item > div.sg-col-inner')
        for searched_work in searched_works:
            work_title = searched_work.select_one('h2.s-line-clamp-4 > a.a-link-normal > span.a-size-base-plus').text
            genre = searched_work.select_one('div.s-price-instructions-style > div:first-of-type > a').text

            if genre == 'Prime Video':
                # タイトル検証アルゴリズム
                cleaned_searched_title = title_convert(work_title)

                if (input_title in cleaned_searched_title):
                    rental_or_free = searched_work.select_one(f'div.a-section > div.a-spacing-top-mini')
                    if rental_or_free:
                        plan = rental_or_free.text
                        if plan == 'プライム会員の方は￥0':
                            result = '見放題'
                            
                        elif plan == 'または、プライム会員は￥0':
                            result = '見放題'

                        elif plan == 'Or ¥0 with a Prime membership':
                            result = '見放題'

                        elif plan == '¥0 with a Prime membership':
                            result = '見放題'
                            
                        else:
                            result = 'レンタル'
                    else:
                        rental_or_none = searched_work.select_one('div.a-section > div.a-spacing-top-micro span.a-size-small')
                        if rental_or_none:
                            result = 'なし'
                        else:
                            result = 'レンタル'
                    break
            
        else:
            result = 'なし'

    except:
        result = '取得失敗'

        
    driver.quit()
    return result, url

        
        



