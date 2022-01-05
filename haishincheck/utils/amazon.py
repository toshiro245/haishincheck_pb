import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def amazon_scraping(driver, title):
    # try:
    true_flag = False
    input_title = title_convert(title)
    title_length = len(input_title)

    url = f"https://www.amazon.co.jp/s?k={title}&i=instant-video"
    driver.get(url)
    time.sleep(4)

    result = 'テスト'

    # elem_search_btn = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div[1]/input")
    # elem_search_btn.clear()
    # time.sleep(1)
    # elem_search_btn.send_keys(title)
    # click_icon = driver.find_element(By.CSS_SELECTOR, '#nav-search-submit-button')
    # driver.execute_script('arguments[0].click();', click_icon)
    # time.sleep(5)


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
            
            if title_length <= 7:
                # 完全一致しているか
                if (input_title in cleaned_searched_title):
                    true_flag = True
            
            else:
                # 70％以上一致しているか
                title_length_70percent = int(round(title_length * 0.7, 0))
                for initial, last in enumerate(range(title_length_70percent, title_length+1)):
                    confirmed_title = input_title[initial:last]
                    if (confirmed_title in cleaned_searched_title):
                        true_flag = True
                        break


            # レンタルかどうか
            if true_flag:
                rental_or_free = searched_work.select_one(f'div.a-section > div.a-spacing-top-mini')
                if rental_or_free:
                    plan = rental_or_free.text
                    if plan == 'プライム会員の方は￥0':
                        result = '見放題'
                        
                    elif plan == 'または、プライム会員は￥0':
                        result = '見放題'
                        
                    else:
                        result = 'レンタル'
                else:
                    result = 'レンタル'
                break
        
    else:
        result = 'なし'

    # except:
    #     result = 'エラー'

        
    driver.quit()
    return result

        
        



