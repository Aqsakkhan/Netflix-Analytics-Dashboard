import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

# Dashboard Title
st.title("🎬 Netflix Content Insights")
st.caption(
    "Interactive dashboard for exploring Netflix content trends, ratings, genres, countries, and growth patterns."
)

# Load Dataset
df = pd.read_csv("netflix_titles.csv")

st.sidebar.title("Filters")

st.sidebar.markdown("---")
st.sidebar.info(
    """
    🎬 Netflix Content Insights

    Interactive dashboard for exploring
    Netflix content trends, ratings,
    countries, genres, and growth.
    """
)

# Content Type Filter
content_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
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

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Total Titles", total_titles)
kpi2.metric("Movies", movies)
kpi3.metric("TV Shows", tv_shows)
 
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Movies vs TV Shows")

    type_counts = filtered_df["type"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(type_counts.index, type_counts.values)

    ax.set_xlabel("Content Type")
    ax.set_ylabel("Number of Titles")

    for i, v in enumerate(type_counts.values):
        ax.text(i, v + 50, str(v), ha="center")

    st.pyplot(fig)

with col2:
    st.subheader("⭐ Content Ratings Distribution")

    rating_counts = (
        filtered_df["rating"]
        .dropna()
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(rating_counts.index, rating_counts.values)

    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of Titles")

    for i, v in enumerate(rating_counts.values):
        ax.text(i, v + 10, str(v), ha="center")

    plt.xticks(rotation=45)

    st.pyplot(fig)

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌍 Top Countries Producing Netflix Content")

    country_counts = (
        filtered_df["country"]
        .dropna()
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.barh(country_counts.index, country_counts.values)

    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Country")

    st.pyplot(fig)

with col4:
    st.subheader("🎭 Most Popular Genres")

    genres = (
        filtered_df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    genre_counts = genres.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.barh(genre_counts.index, genre_counts.values)

    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Genre")

    st.pyplot(fig)

st.markdown("---")
st.subheader("📈 Netflix Content Growth Over Years")

content_growth = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    content_growth.index,
    content_growth.values,
    marker="o"
)

ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Titles")
ax.set_title("Netflix Content Growth Over Time")

plt.xticks(rotation=45)

st.pyplot(fig)

with st.expander("📋 View Dataset"):
    st.dataframe(filtered_df)

st.markdown("---")
st.caption(
    "Built with Python, Pandas, Matplotlib and Streamlit | Created by Aqsa Khan"
)