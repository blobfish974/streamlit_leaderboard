import altair as alt
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup as bs
import requests
import streamlit as st
import re
import json
from datetime import datetime, timedelta, date
import numpy as np


st.set_page_config(
    page_title="Leaderboard",
    page_icon="images/trophy.png",
)

st.title('Root-me leaderboard')
st.text(" \n")


col1, col2, col3 = st.columns(3)
img_root_me = Image.open(
    "images/root-me.png")
img_telecom = Image.open(
    "images/logo_telecom.png")
with col2:
    st.image([img_root_me, img_telecom], width=100)

st.text(" \n")
status_text = st.empty()
my_bar = st.progress(0)
st.text(" \n")
st.header("Ranking of MS Cyber 2 2021-2022")


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


start_dt = date(2021, 9, 1)
end_dt = date.today()
date_list = list()
for dt in daterange(start_dt, end_dt):
    date_list.append(dt)
    # print(dt.strftime("%Y-%m-%d"))
# print(date_list)
num_dates = len(date_list)


data_names = ["pieacoulisse", "Miaimbouchon","BOUCENNA", "fdn4444","miled","Caroline", "Pompottewi","Arsuol","Yves-Marie"]
data_score = list()
all_scores = np.zeros((num_dates, len(data_names)))
len_data_names = len(data_names)


pattern = "validations.push\({(.+?),[\s]*}\);"


for index, name in enumerate(data_names):
    url = "https://www.root-me.org/" + name + "?inc=statistiques&lang=fr"
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'html.parser')
    h3 = soup.find_all('h3')
    points = int(h3[5].getText().strip())
    # challenges_done = h3[5].getText().strip()
    script = soup.find_all('script', src=None)
    raw_validation_push = re.findall(pattern, script[-1].string, re.S)
    json_struct = json.loads("[ ]")
    if raw_validation_push:
        for i in range(len(raw_validation_push)):
            raw_validation_push[i] = re.sub(
                r"'titre'\s*:.*", " ", raw_validation_push[i])
            json_string = "{" + \
                raw_validation_push[i].replace('\'', '\"') + "\n}"
            # print(json_string)
            data = json.loads(json_string)
            json_struct.append(data)
            print("Success")
        # print(json_struct)
        # Constructing the data array for points according to dates
        score_sum = 0
        scores = [0] * num_dates
        for x in json_struct:
            date_time_str = x["date"]
            date_time_obj = datetime.strptime(
                date_time_str, '%Y-%m-%d %H:%M:%S')
            if(date_time_obj.date() in date_list):
                index_date = date_list.index(date_time_obj.date())
            else:  # it happens when the user had points before the start date
                print("Index not found for " +
                      date_time_obj.date().strftime("%Y-%m-%d"))
                index_date = 0
            score_sum += int(x["score"])
            for j in range(index_date, num_dates):
                scores[j] = score_sum
        print(scores)
        all_scores[:, index] = scores

    else:
        print("Error get stats points")

    data_score.append(points)
    prog = int((index+1)*100/len_data_names)
    status_text.text("%i%% Complete" % prog)
    my_bar.progress(prog)

my_bar.empty()

df_ranking = pd.DataFrame({
    'names': data_names,
    'scores': data_score
})

st.altair_chart(alt.Chart(df_ranking).mark_bar().encode(
    x='scores',
    # y='names',
    y=alt.Y('names', sort='descending'),
))


df_scores = pd.DataFrame(
    all_scores,
    columns=data_names
)

df_scores['date'] = date_list
df_scores = df_scores.set_index('date')

st.header("Score evolution")
st.line_chart(df_scores)

st.subheader("Ranking table")
df_ranking.sort_values(by=["scores"], inplace=True, ascending=False)
df_ranking
st.subheader("Score evolution table")
df_scores
