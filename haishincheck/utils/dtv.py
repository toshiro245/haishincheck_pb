import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def dtv_scraping(driver, title):
    try:
        true_flag = False
        input_title = title_convert(title)
        title_length = len(input_title)
        modified_title = title.replace('%', 'パーセント').replace('％', 'パーセント')
        
        page_url = f"https://video.dmkt-sp.jp/search/?q={modified_title}"
        driver.get(page_url)
        time.sleep(4)


        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')


        searchResultsVideoList = soup.select('li.dup-card-list-grid-max6col-m__item--TmiMC')
        for searchResultsVideo in searchResultsVideoList:
            work_title = searchResultsVideo.select_one('h3.dup-text-ellipsis-default-m__root--1toBF').text
            cleaned_searched_title = title_convert(work_title)

            # 検索アルゴリズム
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
                is_rental = searchResultsVideo.select_one('div.dup-card-grid-item-default-m__rental--1GrDL')
                if is_rental:
                    result = 'レンタル'
                else:
                    result = '見放題'
                break


        else:
            result = 'なし'


    except:
        result = 'エラー'


    return result
