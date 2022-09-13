'''
    Tips to improve:
        This is for educational purposes so didn't create a optimized scraper. Instead of moving to coordination that increased by 400 each time, it should move to last comment's position that rendered. Also using Youtube's API is best case for this scenario but I will learn it later, this is for getting used to selenium.
'''

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
# driver.get('https://www.youtube.com/watch?v=CvJ6Ic3PS7M&ab_channel=AryanSharma')
driver.get('https://www.youtube.com/watch?v=NjOMSJgsh9A&ab_channel=LaptopluGezgin')

# 'ytd-comment-renderer' is class of the objects we are looking for

# class 'published-time-text' must be removed

comments = []
comment_sizes = []
pos = 500
while (True):
    driver.execute_script('window.scrollTo(0, '+str(pos)+');')
    pos += 400
    time.sleep(5)
    comments = driver.find_elements(By.CLASS_NAME, 'ytd-comment-renderer')
    comment_sizes.append(len(comments))
    if (len(comment_sizes) > 9):
        is_done = True
        for i in range(len(comment_sizes)-10, len(comment_sizes)-1):
            if (comment_sizes[i] != comment_sizes[i+1]):
                is_done = False
        if (is_done):
            break

comments_updated = []
for item in comments:
    if (item.tag_name == 'yt-formatted-string' and not 'published-time-text' in item.get_attribute('class')):
        comments_updated.append(item)

for item in comments_updated:
    print('------------------------------------')
    print(item.get_attribute('class'))
    print('\n'+item.text)

print('total comments=', len(comments_updated))

print(comment_sizes)

driver.close()
