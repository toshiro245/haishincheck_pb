import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


from haishincheck.utils.title_setting import title_convert



def unext_scraping(driver, title):

    try:
        input_title = title_convert(title)
        URL = f'https://video.unext.jp/freeword?query={title}'
        driver.get(URL)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('div[data-ucn="searchFreewordTitleList-video-titleCard"]')

        true_flag = False
        for work in works:
            searched_title = work.select_one('h3.TitleCard__MetaInfoTitle-sc-1aj72c9-14').text
            
            cleaned_searched_title = title_convert(searched_title)
            title_length = len(input_title)
            if title_length <= 7:
                # 完全一致しているか
                if input_title in cleaned_searched_title:
                    true_flag = True


            else:
                # 70％以上一致しているか
                title_length_70percent = int(round(title_length * 0.7, 0))
                for initial, last in enumerate(range(title_length_70percent, title_length+1)):
                    confirmed_title = input_title[initial:last]
                    if confirmed_title in cleaned_searched_title:
                        true_flag = True
                        break

            if true_flag:
                is_rental = work.select_one("article.TitleCard__TitleCardContainer-sc-1aj72c9-0 div.Icon__IconContainer-shsrka-0 #guide_global_badge_points_svg__exportables")
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

