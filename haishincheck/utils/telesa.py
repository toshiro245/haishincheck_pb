import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert


def telesa_scraping(driver, title):
    try:
        true_flag = False
        input_title = title_convert(title)
        title_length = len(input_title)
        
        page_url = f'https://www.telasa.jp/search?q={title}'
        driver.get(page_url)
        time.sleep(5)

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
                    break

            if true_flag:
                break


        else:
            result = 'なし'
    
    except:
        result = 'エラー'


    driver.quit()
    return result
