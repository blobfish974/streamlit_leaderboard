import streamlit as st
import json
import numpy as np
import pandas as pd
import altair as alt


json_string = "[{'date': '2021-11-19 15:24:34', 'difficulte': 1, 'score': 5}, {'date': '2021-11-19 15:33:45', 'difficulte': 1, 'score': 5}, {'date': '2021-11-19 15:48:58', 'difficulte': 1, 'score': 10}, {'date': '2021-11-19 15:52:50', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 14:43:12', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 15:03:35', 'difficulte': 2, 'score': 15}, {'date': '2021-11-21 17:47:52', 'difficulte': 2, 'score': 15}, {'date': '2021-12-11 19:34:26', 'difficulte': 1, 'score': 5}, {'date': '2021-12-11 19:49:45', 'difficulte': 1, 'score': 5}, {'date': '2021-12-11 20:04:31', 'difficulte': 1, 'score': 5}, {'date': '2021-12-15 14:47:57', 'difficulte': 1, 'score': 5}, {'date': '2021-12-15 15:36:48', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 08:48:04', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 08:54:42', 'difficulte': 1, 'score': 5}, {'date': '2022-01-13 09:05:53', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 10:17:22', 'difficulte': 2, 'score': 20}, {'date': '2022-01-13 10:22:00', 'difficulte': 2, 'score': 15}, {'date': '2022-01-13 11:06:36', 'difficulte': 1, 'score': 10}, {'date': '2022-01-13 11:16:01', 'difficulte': 1, 'score': 10}]"
json_string = json_string.replace('\'', '\"')
data = json.loads(json_string)
data2 = json.loads(json_string)
json_array = [data, data2]
# print(data)
# last_rows = np.random.randn(1, 3)  # [[ 0.40272379  3.30793732 -0.43315649]]
# last_rows = [[0]]
dates = list()
scores = list()
# chart = st.line_chart(last_rows)
for x in data:
    # print(x["date"])
    # new_rows = last_rows + x["score"]
    # chart.add_rows(new_rows)
    # last_rows = new_rows
    dates.append(x["date"])
    if(len(scores) == 0):
        scores.append(int(x["score"]))
    else:
        scores.append(scores[-1]+int(x["score"]))
print(dates)
print(scores)

df1 = pd.DataFrame({
    'dates': dates,
    'scores': scores,
    # columns=dates)
    # 'y': ('col %d' % i for i in range(len(scores)))})
})
df1
df1.astype({'scores': 'int32'})
df1['dates'] = pd.to_datetime(df1['dates'], format='%Y-%m-%d %H:%M:%S')

st.altair_chart(alt.Chart(df1).mark_line().encode(
    x='dates:T',
    y='scores:Q'
))


# my_table = st.table(df1)
# my_chart = st.line_chart(df1)
"""
df2 = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

my_table.add_rows(df2)
my_chart.add_rows(df2)
"""
