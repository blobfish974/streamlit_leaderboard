import json
import altair as alt
import pandas as pd
from PIL import Image
import streamlit as st
import time
import random
import re
import requests
from datetime import datetime, timedelta, date
import numpy as np
from bs4 import BeautifulSoup as bs

WAIT_SECONDS = 60 * 1  # update every 10 minutes

st.set_page_config(
    page_title="Leaderboard",
    page_icon="images/trophy.png",
    layout="wide"
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

with open("updated_file.txt", "r") as txt_file:
    updated = txt_file.read()
    st.text("Last update: " + updated)

st.text(" \n")
st.header("Ranking of MS Cyber 2 2021-2022")


df_ranking = pd.read_csv('df_ranking.csv', index_col=0, sep="\t")

df_ranking.sort_values(by=["scores"], inplace=True, ascending=False)
df_ranking = df_ranking.reset_index(drop=True)
df_ranking.index = df_ranking.index + 1

st.altair_chart(alt.Chart(df_ranking).mark_bar().encode(
    x='scores',
    # y='names',
    # y=alt.Y('names', sort='descending'),
    y=alt.Y('names', sort=None),
))


df_scores = pd.read_csv('df_scores.csv', index_col=0, sep="\t")


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


start_dt = date(2021, 9, 1)
end_dt = date.today()
date_list = list()
for dt in daterange(start_dt, end_dt):
    date_list.append(dt)
num_dates = len(date_list)

df_scores['date'] = date_list
df_scores = df_scores.set_index('date')

st.header("Score evolution")
st.line_chart(df_scores)
st.header("Score evolution last month")
df_scores_last_month = df_scores.iloc[-30:, :]
st.line_chart(df_scores_last_month)

st.subheader("Ranking table")
df_ranking
st.subheader("Score evolution table")
df_scores


def update_df_ranking(df, df_updated):
    print("Enter update_df_ranking")
    for index, row in df_updated.iterrows():
        name = df_updated.loc[index, ['names']]['names']
        index_name = df.index[df['names']
                              == name].tolist()
        if len(index_name) == 0:
            score = df_updated.loc[index, ['scores']]['scores']
            new_row = {'names': name, 'scores': score}
            df = df.append(new_row, ignore_index=True)
        else:
            index_name = index_name[0]
            if(df_updated.loc[index, ['scores']]['scores'] != 0):
                df.loc[index_name, ['scores']
                       ] = df_updated.loc[index, ['scores']]['scores']
    return df


def update():
    print("Enter update")
    start_dt = date(2021, 9, 1)
    end_dt = date.today()
    date_list = list()
    for dt in daterange(start_dt, end_dt):
        date_list.append(dt)
    num_dates = len(date_list)

    # data_names = ["pieacoulisse", "Miaimbouchon", "BOUCENNA"]
    data_names = ["pieacoulisse", "Miaimbouchon", "BOUCENNA", "fdn4444",
                  "miled", "Caroline-46821", "Pompottewi", "Arsuol", "Yves-Marie", "Keyoke", "giso", "Yasuotarie"]
    len_data_names = len(data_names)
    data_score = list()
    # matrix to store all points for each date
    all_scores = np.zeros((num_dates, len(data_names)))

    pattern = "validations.push\({(.+?),[\s]*}\);"

    print("*** Updating datas ***")
    for index, name in enumerate(data_names):
        print("Fetching " + name + "...")
        url = "https://www.root-me.org/" + name + "?inc=statistiques&lang=en"
        time.sleep(3+random.randint(3, 4))

        response = requests.get(url)
        html = response.content
        soup = bs(html, 'html.parser')
        h3 = soup.find_all('h3')
        try:
            points = int(h3[5].getText().strip())
        except:
            print("Error getting score")
            data_score.append(0)
            continue
        else:
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
                    # print("Success")
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
                        # print("Index not found for " +
                        #       date_time_obj.date().strftime("%Y-%m-%d"))
                        index_date = 0
                    score_sum += int(x["score"])
                    for j in range(index_date, num_dates):
                        scores[j] = score_sum
                all_scores[:, index] = scores

            else:
                print("Error getting stats points")

            data_score.append(points)

    df_ranking = pd.read_csv('df_ranking.csv', index_col=0, sep="\t")
    # print(df_ranking)

    df_ranking_updated = pd.DataFrame({
        'names': data_names,
        'scores': data_score
    })
    df_ranking_updated.sort_values(
        by=["scores"], inplace=True, ascending=False)
    # df_ranking_updated.to_csv("df_ranking.csv", sep="\t")
    df_ranking = update_df_ranking(df_ranking, df_ranking_updated)
    df_ranking.to_csv("df_ranking.csv", sep="\t")
    # df_ranking_updated = df_ranking_updated.reset_index(drop=True)
    # df_ranking_updated.index = df_ranking_updated.index + 1
    # print(df_ranking)

    # df_scores = pd.read_csv('df_scores.csv', sep="\t")
    # print(df_scores)

    df_scores_updated = pd.DataFrame(
        all_scores,
        columns=data_names
    )

    df_scores_updated['date'] = date_list
    df_scores_updated = df_scores_updated.set_index('date')
    # update_df_scores(df_scores, df_scores_updated)
    # df_scores.to_csv("df_scores.csv", sep="\t")
    df_scores_updated.to_csv("df_scores.csv", sep="\t")
    # print(df_scores_updated)

    # print(time.ctime())
    file = open("updated_file.txt", "w")
    now = datetime.now() + timedelta(hours=1)
    file.write(now.strftime("%d/%m/%Y %H:%M:%S"))
    # threading.Timer(WAIT_SECONDS, foo).start()
    print("...waiting...")
    time.sleep(WAIT_SECONDS)
    update()


st.text(" \n")
st.text(" \n")
st.text("Update logs")


print("Calling updating function")
# leaderboard_time_updated.foo()
update()
