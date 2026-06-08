import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

st.title("🎬 Netflix Analytics Dashboard")

st.write("Explore Netflix content trends and insights.")

df = pd.read_csv("netflix_titles.csv")

st.sidebar.title("Filters")

content_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

# Country Filter
countries = sorted(df["country"].dropna().unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + countries
)

# Rating Filter
ratings = sorted(df["rating"].dropna().unique())

selected_rating = st.sidebar.selectbox(
    "Select Rating",
    ["All"] + ratings
)

filtered_df = df[df["type"].isin(content_type)]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_rating != "All":
    filtered_df = filtered_df[filtered_df["rating"] == selected_rating]

total_titles = len(filtered_df)
movies = len(filtered_df[filtered_df["type"] == "Movie"])
tv_shows = len(filtered_df[filtered_df["type"] == "TV Show"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tv_shows)


st.subheader("Movies vs TV Shows")

type_counts = filtered_df["type"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))

ax.bar(type_counts.index, type_counts.values)

ax.set_xlabel("Content Type")
ax.set_ylabel("Number of Titles")
ax.set_title("Movies vs TV Shows")

for i, v in enumerate(type_counts.values):
    ax.text(i, v + 50, str(v), ha="center")

st.pyplot(fig)

st.subheader("🌍 Top Countries Producing Netflix Content")

country_counts = (
    filtered_df["country"]
    .dropna()
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(figsize=(8,5))

ax.barh(country_counts.index, country_counts.values)

ax.set_title("Top 10 Countries")
ax.set_xlabel("Number of Titles")
ax.set_ylabel("Country")

for i, v in enumerate(country_counts.values):
    ax.text(v + 5, i, str(v), va="center")

st.pyplot(fig)

st.subheader("🎭 Most Popular Genres")

genres = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
)

genre_counts = genres.value_counts().head(10)

fig, ax = plt.subplots(figsize=(8,5))

ax.barh(genre_counts.index, genre_counts.values)

ax.set_title("Top 10 Genres")
ax.set_xlabel("Number of Titles")
ax.set_ylabel("Genre")

for i, v in enumerate(genre_counts.values):
    ax.text(v + 5, i, str(v), va="center")

st.pyplot(fig)

st.subheader("📈 Netflix Content Growth Over Years")

content_growth = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    content_growth.index,
    content_growth.values,
    marker="o"
)

ax.set_title("Netflix Content Growth Over Time")
ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Titles")

plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("⭐ Content Ratings Distribution")

rating_counts = (
    filtered_df["rating"]
    .dropna()
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(rating_counts.index, rating_counts.values)

ax.set_title("Top Content Ratings")
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Titles")

for i, v in enumerate(rating_counts.values):
    ax.text(i, v + 10, str(v), ha="center")

st.pyplot(fig)

st.subheader("Dataset Preview")
st.dataframe(filtered_df)