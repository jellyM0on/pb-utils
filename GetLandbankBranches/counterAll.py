from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
import time
import csv

driver = webdriver.Chrome()
link = "https://www.landbank.com/find-us"

print("Opening page: {}".format(link))
driver.get(link)

driver.set_window_size(1280, 720)

print("Selecting options: {}".format(link))
select = Select(driver.find_element(By.ID, 'branch'))
select.select_by_value('1')

time.sleep(25)
provinceForm = driver.find_element(By.ID,'province')
driver.execute_script("arguments[0].disabled = false", provinceForm)

provinceSelect = Select(driver.find_element(By.ID, 'province'))

for optionIndex, option in enumerate(provinceSelect.options): 
    if(optionIndex == 1): continue

    branchesArr = []

    provinceSelect.select_by_index(optionIndex)
    provinceName = f"{provinceSelect.options[optionIndex].text}"
    print(f"Listing {provinceName} branches...")
    time.sleep(30)

    branchList = driver.find_elements(By.XPATH, '//*[@id="branchlistbox"]/div')

    index = 1
    for branch in branchList:
        title = branch.find_element(By.XPATH, f'/html/body/div/section/div/div[1]/div[2]/div/div/div[3]/div/div/div/div/div/div[{index}]/a/h6')
        loc = branch.find_element(By.XPATH, f'/html/body/div/section/div/div[1]/div[2]/div/div/div[3]/div/div/div/div/div/div[{index}]/div/p')

        temp = [provinceName.upper(), index, f"{title.text}", loc.text]
        branchesArr.append(temp)
        index += 1

    with open('./branchesTemp.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerows(branchesArr)
        writer.writerow("-")

print("END")

driver.quit()