import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def tsutaya_scraping(driver, title):
    # try:
    true_flag = False
    input_title = title_convert(title)
    title_length = len(input_title)
    
    page_url = 'https://movie-tsutaya.tsite.jp/netdvd/dvd/top.do'
    driver.get(page_url)
    time.sleep(4)

    # search
    search_bar = driver.find_element(By.CSS_SELECTOR, 'div.input-group > input')
    time.sleep(2)
    search_bar.send_keys(title)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'div.input-group > div.input-group-append').click()
    time.sleep(4)


    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    works = soup.select('#container-product-search > div.card-box-searchdvd')

    for work in works:
        work_title = work.select_one('div.card-body-searchdvd > a').text
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
    

    # except:
    #     result = 'エラー'
    

    return result
