from bs4 import BeautifulSoup as bs
import requests

names = ['pieacoulisse', 'Miaimbouchon']

url = "https://www.root-me.org/Miaimbouchon?inc=score&lang=fr"
response = requests.get(url)
html = response.content

# soup = bs(html, "lxml")
soup = bs(html, 'html.parser')

h3 = soup.find_all('h3')
for a in h3:
    print(a)

points = h3[5].getText().strip()
challenges_done = h3[5].getText().strip()

# with open("scores.txt", "a") as file:
#     file.write(points)
