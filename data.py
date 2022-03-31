from selenium import webdriver 
from bs4 import BeautifulSoup 
import requests
import time 
import csv 
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs" 
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers = ["Brown_dwarf", "Constellation", "Right_ascension", "Declination", "App.mag.","Distance(ly)","Spectral_type","Mass(Mj)","Radius(Rj)","Discovery_year","Star_name", "Distance", "Mass", "Radius"]
stars_data = []
new_stars_data = []

def scrape():   
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "stars"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            stars_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(stars_data)
scrape()

def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_stars_data.append(temp_list)

scrape()

for data in stars_data:
    scrape_more_data(data[5])

final_stars_data = []
for index, data in enumerate(stars_data):
    final_stars_data.append(data + final_stars_data[index])

with open("final.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_stars_data)