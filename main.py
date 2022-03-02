import streamlit as st
import altair as alt
from PIL import Image
import util

st.set_page_config(
    page_title="Leaderboard",
    page_icon="images/trophy.png",
    # layout="wide"
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

data_loaded = util.init_data()
st.text("Last update: " + util.read_last_update())
st.text(" \n")

if(data_loaded):
    st.header("Ranking of MS Cyber 2 2021-2022")
    st.altair_chart(alt.Chart(util.ranking_dataframe()).mark_bar().encode(
        x='scores',
        y=alt.Y('names', sort=None),
        # ))
    ).properties(
        width=500,
        height=400
    ))
    # TODO: add bigger cursor
    # TODO: make figure higher
    st.header("Score evolution")
    st.line_chart(util.scores_dataframe(), width=500, height=600)
    st.header("Score evolution last month")
    st.line_chart(util.scores_last_month_dataframe(), width=500, height=600)
    # TODO: add metrics for 3 best progression over last month
    st.subheader("Ranking table")
    st.dataframe(util.ranking_dataframe())
    st.subheader("Score evolution table")
    st.dataframe(util.scores_dataframe())
else:
    st.write("No data fetched yet")
    st.write("Please reload page when data updating is completed")

# we print what is stored and update at the end (for next user/refresh)
st.write("Data updating...")
util.update_datas()
# TODO: CRON or otherway to automate it
