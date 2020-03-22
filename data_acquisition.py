import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from urllib3.exceptions import MaxRetryError

def get_web_page(web_url):
    # Get the page source of the queue elements.
    driver = webdriver.Chrome(r"C:\Users\kk\Desktop\DataScience\Tutorials\scraper\chromedriver_1.exe")
    queue = [web_url]
    header = ['title', 'year', 'summary', 'credits']
    links = []
    counter = 0
    results = pd.DataFrame(columns=header)

    while (len(queue) > 0 and counter <= 20):
        driver.get(queue[0])
        print("Successfully got the {}th movie page.".format(counter))
        del(queue[0])
        
        # Find the links to other movies.
        try:
            link = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='title_recs']/div[1]/div/div[2]/div[1]/div/a")))
            links += link 
            # Update the queue.
            for link in links:
                queue.append(str(link.get_attribute('href')))
            links = []
        except (TimeoutError, StaleElementReferenceException):
            pass

        # Save some indentification data.
        title = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1')
        year = driver.find_element_by_id('titleYear')
        summary = driver.find_element_by_class_name('summary_text')
        credit = driver.find_element_by_class_name('credit_summary_item')
        
        # Write the data into respective files
        if title.text not in results.title.values:
            t = title.text
            results = results.append({'title':title.text, 'year':year.text, 'summary':summary.text, 'credits':credit.text}, ignore_index=True)
            
            # Obtain the comments.
            comment_section = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='titleUserReviewsTeaser']/div/a[2]")))
            comments = get_comment(comment_section[0].get_attribute('href'), driver)
            with open(r'C:\Users\kk\Desktop\DataScience\MachineLearningProjects\IMDbMovieReview\comments_of_{}.txt'.format(t), 'w+', encoding="utf-8") as f:
                for comment in comments:    
                    f.write('\n')
                    f.write(comment)
                    f.write('\n')
            print("The comments of {} has been recorded.".format(t))
            counter += 1
        else:
            pass
        
        
    df =  pd.DataFrame.from_dict(results)

    df.to_csv(r'C:\Users\kk\Desktop\DataScience\MachineLearningProjects\IMDbMovieReview\IMDb_information.txt', header=None, index=None, sep=' ', mode='a')

    driver.close()


def get_comment(url, driver):
    
    # Get the comment section of each page.
    list_content = []
    c = 0
    driver.get(url)

    try:
        # Click the load-more button.
        while True and c < 15:
            try:
                c += 1
                loadMoreButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'load-more-trigger')))
                time.sleep(2)
                loadMoreButton.click()
                print("The {}th time".format(c))
                time.sleep(5)
            except Exception:
                break

        # Get the comment texts using bs4.
        try:
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            content = soup.find_all('div', class_=['text', 'show-more_control'])
            list_content = [c.get_text() for c in content]
        except Exception:
            pass

        pass
        time.sleep(5)
        
    except Exception:
        pass

    return list_content


get_web_page("https://www.imdb.com/title/tt1517451/?ref_=tt_rec_tti")
