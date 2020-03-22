from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
testurl = "https://www.imdb.com/title/tt0357277/reviews?ref_=tt_urv"
patience_time1 = 60
XPATH_loadmore = "//*[@id='load-more-trigger']"
XPATH_grade = "//*[@class='review-container']/div[1]"
list_grades = []

driver = webdriver.Chrome(r"C:\Users\kk\Desktop\DataScience\Tutorials\scraper\chromedriver_1.exe")
driver.get(testurl)

# This is the part in which I open all 'load more' buttons.
while True:
    try:
        loadmore = driver.find_element_by_id("load-more-trigger")
        time.sleep(2)
        loadmore.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        break
    print("Complete")
    time.sleep(10)

    # When the whole page is loaded, I want to get all 'content' parts.
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    content = soup.find_all('div', class_=['text','show-more__control'])
    list_content = [tag.get_text() for tag in content] 
    
print(list_content)
driver.quit()