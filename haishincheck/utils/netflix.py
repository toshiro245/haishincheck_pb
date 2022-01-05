import time
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from haishincheck.utils.title_setting import title_convert


def netflix_scraping(driver, title):
    try:
        # Netflixログイン情報
        Id = 'r6897327@gmail.com'
        Pass = 'fujimon4372'

        true_flag = False
        input_title = title_convert(title)
        title_length = len(input_title)
        
        base_url = "https://www.netflix.com/browse"
        driver.get(base_url)
        time.sleep(4)

        #ログイン
        login = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div[1]/div/label/input')
        login.send_keys(Id)
        time.sleep(1)

        login = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div[1]/div/label/input')
        login.send_keys(Pass)
        time.sleep(1)

        # driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[1]/form/button').click()
        driver.find_element(By.CSS_SELECTOR, 'form.login-form > button.login-button').click()
        time.sleep(2)

        #アカウントの選択
        # driver_wait = WebDriverWait(driver,10)
        # driver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/span'))).click()
        
        driver.find_element(By.CSS_SELECTOR, 'ul.choose-profile > li:first-of-type span').click()
        time.sleep(2)

        page_url = f'https://www.netflix.com/search?q={title}'
        driver.get(page_url)
        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        works = soup.select('div.galleryContent div.ptrack-content > a')[:10]
        for work in works:
            work_title = work.get('aria-label')
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
                result = '見放題'
                break

        else:
            result = 'なし'
    
    except:
        result = 'エラー'


    driver.quit()
    return result
