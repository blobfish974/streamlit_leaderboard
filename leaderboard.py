import altair as alt
import leaderboard as st
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup as bs
import requests
import streamlit as st

st.title('Root-me leaderboard')
st.text(" \n")


col1, col2, col3 = st.columns(3)
img_root_me = Image.open(
    "D:/programming/projects/root_me_leaderboard/root-me.png")
img_telecom = Image.open(
    "D:/programming/projects/root_me_leaderboard/logo_telecom.png")
# with col1:
#     st.image(img_root_me, width=200)
with col2:
    # st.image(img_telecom, width=200)
    st.image([img_root_me, img_telecom], width=100)

st.text(" \n")
st.text("Ranking of MS Cyber 2 2021-2022")

# Add histogram data
data_names = ["pieacoulisse", "Miaimbouchon"]
data_score = list()
# p = int('3')
# data_score.append(p)
# data_score

status_text = st.empty()
my_bar = st.progress(0)
len_data_names = len(data_names)

for index, name in enumerate(data_names):
    # url = "https://www.root-me.org/" + name + "?inc=score&lang=fr"
    # response = requests.get(url)
    # html = response.content
    # soup = bs(html, 'html.parser')
    # h3 = soup.find_all('h3')
    # points = int(h3[5].getText().strip())
    # challenges_done = h3[5].getText().strip()
    points = 100
    data_score.append(points)
    prog = int((index+1)*100/len_data_names)
    status_text.text("%i%% Complete" % prog)
    my_bar.progress(prog)
my_bar.empty()

source = pd.DataFrame({
    'names': data_names,
    'scores': data_score
})
# source.sort_values(by=["scores"], inplace=True, ascending=False)
# source

st.altair_chart(alt.Chart(source).mark_bar().encode(
    x='scores',
    # y='names',
    y=alt.Y('names', sort='descending'),
))

# source.sort_values(by=["scores"], inplace=True, ascending=False)
# source
