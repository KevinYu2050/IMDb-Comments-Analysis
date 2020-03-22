# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# from urllib3.exceptions import NewConnectionError, MaxRetryError



# patience_time1 = 60
# XPATH_loadmore ="//*[@id='load-more-trigger']"
# XPATH_grade ="//*[@class='review-container']/div[1]"
# list_grades = []

def get_comment(url, driver):
    list_content = []
    c = 0
    driver.get(url)
    print("Success.")

    try:
        while c <= 5:
            try:
                c += 1
                loadMoreButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'load-more-trigger')))
                time.sleep(2)
                loadMoreButton.click()
                print("The {}th time".format(c))
                time.sleep(5)
            except Exception:
                break

        try:
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            print("bs4!")
            content = soup.find_all('div', class_=['text', 'show-more_control'])
            list_content = [c.get_text() for c in content]
        except Exception:
            pass
        
        pass
        print("Complete.")
        time.sleep(5)
        
    except Exception:
        pass
    
    # try:
    #     WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'content')))
        
    #     review = driver.find_elements_by_xpath('//*[@id="main"]/section/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[1]')
    #     for r in review:
    #         content.append(r.text)
    # except TimeoutException:
    #     pass

    return list_content

driver = webdriver.Chrome(r"C:\Users\kk\Desktop\DataScience\Tutorials\scraper\chromedriver_1.exe")
driver.get("https://www.imdb.com/title/tt1517451/?ref_=tt_rec_tti")


comment_section = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='titleUserReviewsTeaser']/div/a[2]")))
print(str(comment_section[0].get_attribute('href')))
comments = get_comment(comment_section[0].get_attribute('href'), driver)
print(comments)
print("Let it roll!")        



with open(r'C:\Users\kk\Desktop\DataScience\MachineLearningProjects\IMDbMovieReview\comments.txt', 'w+', encoding="utf-8") as f:
    for comment in comments:
        f.write('\n')
        f.write(comment)
        f.write('\n')

driver.quit()

