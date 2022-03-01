import streamlit as st
import altair as alt
from PIL import Image
import util

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

util.init_data()
st.text("Last update: " + util.read_last_update())
st.text(" \n")

st.header("Ranking of MS Cyber 2 2021-2022")

st.altair_chart(alt.Chart(util.ranking_dataframe()).mark_bar().encode(
    x='scores',
    y=alt.Y('names', sort=None),
))

st.header("Score evolution")
st.line_chart(util.scores_dataframe())

st.header("Score evolution last month")
st.line_chart(util.scores_last_month_dataframe())

st.subheader("Ranking table")
st.dataframe(util.ranking_dataframe())

st.subheader("Score evolution table")
st.dataframe(util.scores_dataframe())

# we print what is stored and update at the end (for next user/refresh)
util.update_datas()
