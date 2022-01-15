import plotly.express as px
import leaderboard as st
import pandas as pd

# https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart
import plotly.figure_factory as ff
import numpy as np

# Add histogram data
x1 = 30
x2 = 10

# Group data together
data_score = [x1, x2]
data_names = ["pieacoulisse", "Miaimbouchon"]
# data = [data_score, data_names]
# data
d = {'score': data_score, 'name': data_names}
df2 = pd.DataFrame(data=d)
df2
# st.bar_chart(df2)
# st.bar_chart(df2)

print(np.random.randn(50, 3))

chart_data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["a", "b", "c"])
chart_data
st.bar_chart(chart_data)


"""
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2
hist_data = [x1, x2, x3]
group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
    hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)"""

# https://discuss.streamlit.io/t/how-to-create-a-horizontal-bar-chart-with-streamlit/18162/2
# df = pd.DataFrame(data, columns=['score', 'name'])
# df = pd.DataFrame(data)
fig = px.bar(df2, orientation='h')
st.write(fig)

# Hello example
"""
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
"""
