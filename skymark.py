# coding:utf-8

# コマンド実行例
# python3 skymark.py h f 9 21

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sys
import time

TIME_TO_WAIT = 1

driver = webdriver.Chrome()

url = "https://www.res.skymark.co.jp/sp/inputdatecond?r_ad=top"
driver.get(url)
time.sleep(TIME_TO_WAIT)

argv1 = sys.argv[1]
argv2 = sys.argv[2]

location_map = {
    'f': '福岡',
    'h': '羽田'
}

dep_to_select = location_map[argv1]
arr_to_select = location_map[argv2]

month_to_select = sys.argv[3]
day_to_select = sys.argv[4]

month_element = driver.find_element("name", "month")
Select(month_element).select_by_value(month_to_select)

day_element = driver.find_element("name", "day")
Select(day_element).select_by_value(day_to_select)

driver.find_element(By.XPATH, "//span[@id='dep']").click()
time.sleep(TIME_TO_WAIT)

driver.find_element(By.XPATH, "//a[contains(text(), '" + dep_to_select + "')]").click()
time.sleep(TIME_TO_WAIT)

driver.find_element(By.XPATH, "//span[@id='arr']").click()
time.sleep(TIME_TO_WAIT)

element_arr = driver.find_element(By.XPATH, "//a[contains(text(), '" + arr_to_select + "')]")
driver.execute_script("arguments[0].click();", element_arr)
time.sleep(TIME_TO_WAIT)

driver.find_element(By.XPATH, "//input[@value='検索']").click()
time.sleep(TIME_TO_WAIT)

links = driver.find_elements(By.XPATH, "//a[.//span[@id='disFlightInfo']]")

for link in links:
    driver.execute_script("arguments[0].click();", link)
    time.sleep(TIME_TO_WAIT)
    
    fare_statuses= link.find_element("xpath", "./../..").find_elements(By.CLASS_NAME, "fareStatus")

    for fare_status in fare_statuses:
        fare_name = fare_status.find_element("xpath", "./..").find_element(By.CLASS_NAME, "fareName").text
        if "普通運賃" in fare_name:
            flight_info = link.find_element("id", "disFlightInfo").text
            yen_index = flight_info.find("¥")
            flight_info_trimmed = flight_info[:yen_index]
            print(f"Flight Info: {flight_info_trimmed}残席: {fare_status.text}\n")

input("Enterキーを押すとブラウザを閉じます...")