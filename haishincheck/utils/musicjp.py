import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def musicjp_scraping(driver, title):
    try:
        true_flag = False
        input_title = title_convert(title)
        title_length = len(input_title)
        
        page_url = f"https://music-book.jp/video/search/title?keyword={title}"
        driver.get(page_url)
        time.sleep(4)


        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('div.image-list-item')

        for work in works:
            work_title = work.select_one('p.title').text
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

            if true_flag:
                result = 'レンタル'
                break


        else:
            result = 'なし'


    except:
        result = 'エラー'
    

    return result
