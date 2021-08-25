from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import os
from time import strftime
import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import requests

chrome_driver_path = "/Users/johnchen/Dropbox/My Mac (Johns-Air)/Downloads/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)


if __name__ == '__main__':
    url = 'http://www.cloudping.info/'
    aws_latency = dict()
    try:
        #driver = webdriver.Chrome(executable_path='./chromedriver')
        # Webdriver 的執行檔也可以使用 PhantomJS
        # driver = webdriver.PhantomJS('./phantomjs')

        driver.maximize_window()
        driver.set_page_load_timeout(60)
        driver.get(url)

        # 定位日期輸入欄位, 並輸入日期
        #element = driver.find_element_by_id('fromdate_TextBox')
        #element.send_keys('1010101')
        #element = driver.find_element_by_id('todate_TextBox')
        #element.send_keys('1060101')

        # 定位選單所在欄位並點擊
        driver.find_element_by_id('pingbutton').click()

        # 巡覽選單, 點擊對應選項
        #for option in driver.find_elements_by_tag_name('option'):
            #if option.text == '其他':
                #option.click()

        # 點擊送出按鈕
        #element = driver.find_element_by_id('Submit_Button').click()

        # 等待目標表格出現
        #element = WebDriverWait(driver, 60).until(
            #expected_conditions.presence_of_element_located((By.ID, 'us-gov-west-1'))
        #)
        
        element = WebDriverWait(driver, 600).until(
            expected_conditions.element_to_be_clickable((By.ID, 'pingbutton'))
        )

        # page_source 可以回傳目前瀏覽器所看到的網頁文件
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find(id='content')
        regions = table.find_all('td',class_='')
        latency = table.find_all('td',class_='latency')

        for i in range(len(regions)-2):
        	#if row.text:
        	print (regions[i].text,latency[i].text)
        	aws_latency[regions[i].text] = latency[i].text

        	#print (latency[i])

        #print (table.find_all('td').text)
        #for row in table.find_all('tr'):
            #aws_latency.update(row.stripped_strings)
            #print([s for s in row.stripped_strings])
        now = strftime('%Y-%m-%d %H:%M:%S')
        aws_latency = json.dumps(aws_latency)
        with open("./log/"+now+".txt", 'w') as f:
        	f.write(aws_latency)
    finally:
        driver.quit()  # 關閉瀏覽器, 結束 webdriver process

    headers = {
        'Authorization': 'Bearer mrlPP0HF4OoPp7rLtMwk3sMkHhnqRfNOdjejUzthHz3'
        }

    data = {
        'message': aws_latency
    }
    url = 'https://notify-api.line.me/api/notify'

    res = requests.post(url, data=data, headers=headers)
    print(res)    


