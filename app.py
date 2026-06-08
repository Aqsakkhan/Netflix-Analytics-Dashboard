import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

st.title("🎬 Netflix Analytics Dashboard")

st.write("Explore Netflix content trends and insights.")

df = pd.read_csv("netflix_titles.csv")

total_titles = len(df)
movies = len(df[df["type"] == "Movie"])
tv_shows = len(df[df["type"] == "TV Show"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tv_shows)

st.subheader("Dataset Preview")
st.dataframe(df.head())