import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

url = 'https://www.youtube.com/watch?v=KYKGFujJp6Y'  # youtube video link
executable_path = r"C:\Program Files\Web drivers\chromedriver.exe"  # web driver executable path
num_comments = 100  # number of comments you need

current_position = 0
comments_data = []

# open new Chrome browser
driver = webdriver.Chrome(executable_path=executable_path)  # if you are using firefox, webdriver.Firefox(executable_path=executable_path)
driver.get(url)


# for scroll the website
def scroll():
    end = current_position + 500
    driver.execute_script("window.scrollTo({}, {});".format(current_position, end))
    time.sleep(2)
    return end


# for get numeric value from count text
def get_num(text):
    if text is not None:
        return int(''.join(re.findall(r'\d', text)))
    else:
        return 0


current_position = scroll()

# get total comment count
cmt_count_elm = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/yt-formatted-string')))
total_comment_count = get_num(cmt_count_elm.text)

while True:
    comments = driver.find_elements_by_xpath('//*[@id="comment"]')
    length = len(comments)
    print('please wait ....[{}/{}]'.format(length, total_comment_count))
    if length >= num_comments:
        break
    current_position = scroll()

for c in comments:
    try:
        comments_data.append({
            'comment': c.find_element_by_id('content-text').text,
            'author': c.find_element_by_id('author-text').text,
            'vote': c.find_element_by_id('vote-count-middle').text,
        })
    except:
        print("No such element")

driver.close()
# save as csv
comment_df = pd.DataFrame(comments_data, columns=['comment', 'author', 'vote'])
comment_df.to_csv('comments_data', index=False)
