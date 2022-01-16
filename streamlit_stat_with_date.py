from datetime import datetime, timedelta, date
import json
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


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

json_string = "[{'date': '2021-11-19 15:24:34', 'difficulte': 1, 'score': 5}, {'date': '2021-11-19 15:33:45', 'difficulte': 1, 'score': 5}, {'date': '2021-11-19 15:48:58', 'difficulte': 1, 'score': 10}, {'date': '2021-11-19 15:52:50', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 14:43:12', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 15:03:35', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 17:47:52', 'difficulte': 2, 'score': 15}, {'date': '2021-12-11 19:34:26', 'difficulte': 1, 'score': 5}, {'date': '2021-12-11 19:49:45', 'difficulte': 1, 'score': 5}, {'date': '2021-12-11 20:04:31', 'difficulte': 1, 'score': 5}, {'date': '2021-12-15 14:47:57', 'difficulte': 1, 'score': 5}, {'date': '2021-12-15 15:36:48', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 08:48:04', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 08:54:42', 'difficulte': 1, 'score': 5}, {'date': '2022-01-13 09:05:53', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 10:17:22', 'difficulte': 2, 'score': 20}, {'date': '2022-01-13 10:22:00', 'difficulte': 2, 'score': 15}, {'date': '2022-01-13 11:06:36', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 11:16:01', 'difficulte': 1, 'score': 10}]"
json_string = json_string.replace('\'', '\"')
data = json.loads(json_string)

# chart = st.line_chart(last_rows)
score_sum = 0
scores = [0] * num_dates
# scores = np.zeros((1, num_dates))

print("--- BEGINNING FOR ----")
for x in data:
    date_time_str = x["date"]
    date_time_obj = datetime.strptime(
        date_time_str, '%Y-%m-%d %H:%M:%S')
    print('Date:', date_time_obj.date())
    index = date_list.index(date_time_obj.date())
    # if(date_time_obj.date() in date_list):
    if(index != ValueError):
        print("Index=" + str(index) + " | num_dates=" + str(num_dates))
        score_sum += int(x["score"])
        print(score_sum)
        for j in range(index, num_dates):
            print("scores[" + str(j) + "] = " + str(score_sum))
            scores[j] = score_sum
        print(scores)
    # new_rows = last_rows + x["score"]
    # chart.add_rows(new_rows)
    # last_rows = new_rows
    # dates.append(x["date"])
    # if(len(scores) == 0):
    #     scores.append(int(x["score"]))
    # else:
    #     scores.append(scores[-1]+int(x["score"]))
# print(dates)
print(scores)


df1 = pd.DataFrame({
    'dates': date_list,
    'scores': scores,
    # columns=dates)
    # 'y': ('col %d' % i for i in range(len(scores)))})
})
df1
df1.astype({'scores': 'int32'})
# df1['dates'] = pd.to_datetime(df1['dates'], format='%Y-%m-%d %H:%M:%S')

st.altair_chart(alt.Chart(df1).mark_line().encode(
    x='dates:T',
    y='scores:Q'
))
