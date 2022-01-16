from bs4 import BeautifulSoup as bs
import requests
# from selenium import webdriver
import re
import json

# https://github.com/Franky1/Streamlit-Selenium/blob/main/streamlit_app.py
# https://realpython.com/beautiful-soup-web-scraper-python/
# http://jhroy.ca/uqam/edm5240/BeautifulSoup-DocAbregee.pdf

# url = "https://quotes.toscrape.com/js"
url = "https://www.root-me.org/Miaimbouchon?inc=statistiques&lang=en"

# BS4 VERSION
response = requests.get(url)
html = response.content
soup = bs(html, 'html.parser')
# soup = bs(response.text, 'lxml')
script = soup.find_all('script', src=None)
for j in range(len(script)):
    print("index:" + str(j))
    # print(script[j].string)
    # pattern = "var data =(.+?);\n"
    # pattern = "\"tags\": (.+?);\n"
    # pattern = "vcchart.data =(.+?)];\n"
    # pattern = "validations.push({(.+?)});\n"
    # pattern = "validations.push\({([.\s\S]*),[\s\S]*}"
    # raw_data = re.findall(pattern, script[j].string, re.S)
    # pattern = "validations.push\({([\s\S]*),[\s]*}\);\s*v"
    # raw_data = re.findall(pattern, script[j].string)
    pattern = "validations.push\({(.+?),[\s]*}\);"
    raw_data = re.findall(pattern, script[j].string, re.S)
    # print(raw_data)
    if raw_data:
        for i in range(len(raw_data)):
            print(raw_data[i])
            # json_string = "\"value" + str(i) + "\": {" + raw_data[i] + "}"
            raw_data[i] = re.sub(r"'titre'\s*:.*", " ", raw_data[i])
            json_string = "{" + raw_data[i].replace('\'', '\"') + "\n}"
            print(json_string)
            data = json.loads(json_string)
            print(data)
            # for i in range(len(data)):
            #     print(data[i]['date'])
            print("Success")
    else:
        print("Error")

# SELENIUM VERSION
# driver = webdriver.Chrome()
# driver.get(url)
# soup = bs(driver.page_source, 'lxml')

# auth = soup.find("small", class_="author")
# print(auth.text)
# driver.quit()
