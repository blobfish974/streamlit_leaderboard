import altair as alt
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup as bs
import requests
import streamlit as st

st.title('Root-me leaderboard')
st.text(" \n")


col1, col2, col3 = st.columns(3)
img_root_me = Image.open(
    "root-me.png")
img_telecom = Image.open(
    "logo_telecom.png")
with col2:
    st.image([img_root_me, img_telecom], width=100)

st.text(" \n")
st.text("Ranking of MS Cyber 2 2021-2022")

data_names = ["pieacoulisse", "Miaimbouchon"]
data_score = list()
len_data_names = len(data_names)

status_text = st.empty()
my_bar = st.progress(0)

for index, name in enumerate(data_names):
    url = "https://www.root-me.org/" + name + "?inc=score&lang=fr"
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'html.parser')
    h3 = soup.find_all('h3')
    points = int(h3[5].getText().strip())
    # challenges_done = h3[5].getText().strip()
    # points = 100
    data_score.append(points)
    prog = int((index+1)*100/len_data_names)
    status_text.text("%i%% Complete" % prog)
    my_bar.progress(prog)
my_bar.empty()

source = pd.DataFrame({
    'names': data_names,
    'scores': data_score
})

st.altair_chart(alt.Chart(source).mark_bar().encode(
    x='scores',
    # y='names',
    y=alt.Y('names', sort='descending'),
))

source.sort_values(by=["scores"], inplace=True, ascending=False)
source
