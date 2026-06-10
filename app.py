"""Netflix Content Insights Dashboard.
A portfolio-ready Streamlit dashboard for exploring Netflix catalog trends using
interactive Plotly charts, professional dark styling, and rich filters.
"""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st
# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Netflix Content Insights Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)
# -----------------------------------------------------------------------------
# Theme constants and custom CSS
# -----------------------------------------------------------------------------
NETFLIX_RED = "#E50914"
COLOR_SEQUENCE = [
    "#E50914",
    "#FFB000",
    "#00D1FF",
    "#7C3AED",
    "#22C55E",
    "#F97316",
    "#EC4899",
    "#14B8A6",
]

px.defaults.template = "plotly_dark"
PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#F9FAFB", "family": "Inter, Segoe UI, sans-serif"},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    "margin": {"l": 20, "r": 20, "t": 60, "b": 35},
}

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --netflix-red: #E50914;
            --bg: #0B0F19;
            --panel: #111827;
            --card: #171923;
            --card-border: rgba(255,255,255,0.08);
            --text: #F9FAFB;
            --muted: #9CA3AF;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(229, 9, 20, 0.20), transparent 28rem),
                linear-gradient(135deg, #0B0F19 0%, #111827 55%, #0B0F19 100%);
            color: var(--text);
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0B0F19 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF;
        }

        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            max-width: 1400px;
        }

        .dashboard-header {
            padding: 2.2rem;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(229,9,20,0.92) 0%, rgba(111,12,21,0.86) 42%, rgba(17,24,39,0.96) 100%),
                url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            box-shadow: 0 24px 60px rgba(0,0,0,0.35);
            margin-bottom: 2rem;
        }

        .dashboard-title {
            color: #FFFFFF;
            font-size: clamp(2.1rem, 5vw, 3.6rem);
            font-weight: 800;
            line-height: 1.02;
            margin: 0;
        }

        .dashboard-subtitle {
            color: rgba(255,255,255,0.84);
            font-size: 1rem;
            max-width: 640px;
            margin-top: 0.75rem;
            margin-bottom: 0;
        }

        div[data-testid="stTextInput"] input {
            min-height: 3.25rem;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(17,24,39,0.86);
            color: #FFFFFF;
            font-size: 1rem;
            box-shadow: 0 14px 36px rgba(0,0,0,0.22);
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: rgba(229,9,20,0.75);
            box-shadow: 0 0 0 1px rgba(229,9,20,0.35), 0 18px 42px rgba(229,9,20,0.10);
        }

        .kpi-card {
            min-height: 126px;
            padding: 1.15rem;
            border-radius: 22px;
            border: 1px solid var(--card-border);
            background: linear-gradient(145deg, rgba(23,25,35,0.96), rgba(17,24,39,0.86));
            box-shadow: 0 18px 45px rgba(0,0,0,0.24);
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
        }

        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(229,9,20,0.55);
            box-shadow: 0 24px 60px rgba(229,9,20,0.12);
        }

        .kpi-icon {
            width: 2.6rem;
            height: 2.6rem;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(229,9,20,0.15);
            color: #FFFFFF;
            font-size: 1.35rem;
            margin-bottom: 0.75rem;
        }

        .kpi-label {
            color: var(--muted);
            font-size: 0.86rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0;
        }

        .kpi-value {
            color: #FFFFFF;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1;
        }

        .section-card {
            padding: 0.25rem 0 0.35rem;
            border: 0;
            background: transparent;
            box-shadow: none;
            margin: 1.75rem 0 0.65rem;
        }

        .section-title {
            color: #FFFFFF;
            font-size: 1.15rem;
            font-weight: 750;
            margin-bottom: 0;
        }

        .insight-box {
            border-left: 4px solid var(--netflix-red);
            border-radius: 16px;
            background: rgba(229,9,20,0.09);
            padding: 0.95rem 1.1rem;
            margin: 0.35rem 0 1.8rem;
        }

        .insight-box ul {
            margin-bottom: 0;
        }

        .footer {
            margin-top: 2.25rem;
            padding: 1.1rem;
            border-radius: 18px;
            background: rgba(17,24,39,0.74);
            border: 1px solid rgba(255,255,255,0.08);
            color: var(--muted);
            text-align: center;
        }

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stFormSubmitButton"] > button,
        .stButton > button {
            border-radius: 12px;
            border: 1px solid rgba(229,9,20,0.55);
            background: linear-gradient(135deg, #E50914, #B20710);
            color: #FFFFFF;
            font-weight: 700;
        }

        div[data-testid="stDownloadButton"] > button:hover,
        .stButton > button:hover {
            border-color: #FFFFFF;
            box-shadow: 0 12px 30px rgba(229,9,20,0.22);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }

        hr {
            border-color: rgba(255,255,255,0.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# -----------------------------------------------------------------------------
# Data loading and preparation
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data(path: str = "netflix_titles.csv") -> pd.DataFrame:
    """Load and clean the Netflix titles dataset."""
    data = pd.read_csv(path)
    data["release_year"] = pd.to_numeric(data["release_year"], errors="coerce").astype("Int64")
    data["date_added"] = pd.to_datetime(data["date_added"].str.strip(), errors="coerce")
    data["country"] = data["country"].fillna("Unknown")
    data["rating"] = data["rating"].fillna("Unrated")
    data["listed_in"] = data["listed_in"].fillna("Uncategorized")
    data["director"] = data["director"].fillna("Unknown")
    data["cast"] = data["cast"].fillna("Unknown")
    data["description"] = data["description"].fillna("")
    return data


def split_values(series: pd.Series) -> pd.Series:
    """Split comma-separated values and return a clean exploded Series."""
    return series.dropna().str.split(", ").explode().str.strip()


def render_kpi_card(icon: str, label: str, value: str) -> None:
    """Render a concise KPI card with hover styling."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
def format_number(value: int | float) -> str:
    """Format whole numbers with thousands separators."""
    return f"{int(value):,}"
def apply_common_layout(fig, height: int = 420):
    """Apply consistent Plotly styling."""
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.12)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.12)")
    return fig
df = load_data()
all_countries = sorted(split_values(df["country"]).dropna().unique())
all_ratings = sorted(df["rating"].dropna().unique())
all_genres = sorted(split_values(df["listed_in"]).dropna().unique())
all_types = sorted(df["type"].dropna().unique())
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
# -----------------------------------------------------------------------------
# Sidebar: dashboard context, filters, and download
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("# 🎬 Netflix Insights")
    with st.expander("About", expanded=False):
       st.markdown("""
        Explore Netflix content trends,
        genres, ratings, and countries
        through interactive analytics.
""")
    st.markdown("---")
    st.markdown("### Filters")
    selected_types = st.multiselect(
        "Content Type",
        options=all_types,
        default=all_types,
        help="Choose Movies, TV Shows, or both.",
    )
    selected_year_range = st.slider(
        "Release Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Filter content by original release year.",
    )
    selected_countries = st.multiselect(
        "Countries",
        options=all_countries,
        default=[],
        help="Leave empty to include all countries. Multi-country titles are matched if any selected country appears.",
    )
    selected_ratings = st.multiselect(
        "Ratings",
        options=all_ratings,
        default=[],
        help="Leave empty to include all ratings.",
    )
    selected_genres = st.multiselect(
        "Genres",
        options=all_genres,
        default=[],
        help="Leave empty to include all genres. Titles are matched when they include any selected genre.",
    )
# -----------------------------------------------------------------------------
# Dashboard header
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">Netflix Content Insights Dashboard</h1>
        <p class="dashboard-subtitle">Explore content mix, ratings, countries, genres, and release trends.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
title_search = st.text_input(
    "Search by Title",
    placeholder="🔍 Search Netflix titles...",
    label_visibility="collapsed",
    help="Search by title. Results update every KPI and chart.",
)
# -----------------------------------------------------------------------------
# Filtering logic
# -----------------------------------------------------------------------------
filtered_df = df.copy()

if selected_types:
    filtered_df = filtered_df[filtered_df["type"].isin(selected_types)]
else:
    filtered_df = filtered_df.iloc[0:0]

filtered_df = filtered_df[
    filtered_df["release_year"].between(selected_year_range[0], selected_year_range[1], inclusive="both")
]

if title_search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(title_search.strip(), case=False, na=False, regex=False)
    ]

if selected_countries:
    filtered_df = filtered_df[
        filtered_df["country"].apply(
            lambda value: any(country in [item.strip() for item in str(value).split(",")] for country in selected_countries)
        )
    ]

if selected_ratings:
    filtered_df = filtered_df[filtered_df["rating"].isin(selected_ratings)]

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["listed_in"].apply(
            lambda value: any(genre in [item.strip() for item in str(value).split(",")] for genre in selected_genres)
        )
    ]

filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")

with st.sidebar:
    st.markdown("---")
    st.markdown("### 📥 Export")
    st.download_button(
        label="Download Filtered CSV",
        data=filtered_csv,
        file_name="netflix_filtered_content.csv",
        mime="text/csv",
        use_container_width=True,
        disabled=filtered_df.empty,
    )
# -----------------------------------------------------------------------------
# KPI cards
# -----------------------------------------------------------------------------
total_titles = len(filtered_df)
movies = int((filtered_df["type"] == "Movie").sum())
tv_shows = int((filtered_df["type"] == "TV Show").sum())
unique_countries = split_values(filtered_df["country"]).nunique() if not filtered_df.empty else 0

kpi_cols = st.columns(4)
with kpi_cols[0]:
    render_kpi_card("🎞️", "Total Titles", format_number(total_titles))
with kpi_cols[1]:
    render_kpi_card("🍿", "Movies", format_number(movies))
with kpi_cols[2]:
    render_kpi_card("📺", "TV Shows", format_number(tv_shows))
with kpi_cols[3]:
    render_kpi_card("🌍", "Countries", format_number(unique_countries))


# -----------------------------------------------------------------------------
# Summary insights
# -----------------------------------------------------------------------------
st.markdown("### Insights")

if filtered_df.empty:
    st.warning("No titles match the selected filters. Adjust the sidebar controls to view insights and charts.")
else:
    top_type = filtered_df["type"].value_counts().idxmax()
    top_rating = filtered_df["rating"].value_counts().idxmax()
    top_country = split_values(filtered_df["country"]).value_counts().idxmax()
    top_genre = split_values(filtered_df["listed_in"]).value_counts().idxmax()
    peak_year = int(filtered_df["release_year"].value_counts().idxmax())

    st.markdown(
        f"""
        <div class="insight-box">
            <ul>
                <li><strong>{top_type}</strong> dominate the Netflix catalog</li>
                <li><strong>{top_rating}</strong> is the most common rating.</li>
                <li><strong>{top_genre}</strong> is the top genre.</li>
                <li><strong>{top_country}</strong> is the top country, with peak releases in <strong>{peak_year}</strong>.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
# -----------------------------------------------------------------------------
# Interactive visualizations
# -----------------------------------------------------------------------------
def section_header(title: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
if not filtered_df.empty:
    chart_col_1, chart_col_2 = st.columns(2)

    with chart_col_1:
        section_header("📊 Movies vs TV Shows")
        type_counts = filtered_df["type"].value_counts().reset_index()
        type_counts.columns = ["type", "titles"]
        fig_type = px.pie(
            type_counts,
            names="type",
            values="titles",
            hole=0.48,
            color="type",
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        fig_type.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Titles: %{value:,}<br>Share: %{percent}<extra></extra>",
        )
        st.plotly_chart(apply_common_layout(fig_type), use_container_width=True)

    with chart_col_2:
        section_header("⭐ Content Ratings")
        rating_counts = filtered_df["rating"].value_counts().head(10).reset_index()
        rating_counts.columns = ["rating", "titles"]
        fig_rating = px.bar(
            rating_counts,
            x="rating",
            y="titles",
            color="rating",
            color_discrete_sequence=COLOR_SEQUENCE,
            text="titles",
            labels={"rating": "Rating", "titles": "Number of Titles"},
        )
        fig_rating.update_traces(
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Titles: %{y:,}<extra></extra>",
        )
        st.plotly_chart(apply_common_layout(fig_rating), use_container_width=True)

    chart_col_3, chart_col_4 = st.columns(2)

    with chart_col_3:
        section_header("🌍 Top Countries")
        country_counts = split_values(filtered_df["country"]).value_counts().head(10).sort_values().reset_index()
        country_counts.columns = ["country", "titles"]
        fig_country = px.bar(
            country_counts,
            x="titles",
            y="country",
            orientation="h",
            color="titles",
            color_continuous_scale=["#3B0A0E", NETFLIX_RED, "#FFB000"],
            text="titles",
            labels={"country": "Country", "titles": "Number of Titles"},
        )
        fig_country.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Titles: %{x:,}<extra></extra>",
        )
        fig_country.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_common_layout(fig_country), use_container_width=True)

    with chart_col_4:
        section_header("🎭 Popular Genres")
        genre_counts = split_values(filtered_df["listed_in"]).value_counts().head(10).sort_values().reset_index()
        genre_counts.columns = ["genre", "titles"]
        fig_genre = px.bar(
            genre_counts,
            x="titles",
            y="genre",
            orientation="h",
            color="titles",
            color_continuous_scale=["#111827", "#7C3AED", "#00D1FF"],
            text="titles",
            labels={"genre": "Genre", "titles": "Number of Titles"},
        )
        fig_genre.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Titles: %{x:,}<extra></extra>",
        )
        fig_genre.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_common_layout(fig_genre), use_container_width=True)

    section_header("📈 Content Growth Over Time")
    content_growth = filtered_df.groupby(["release_year", "type"]).size().reset_index(name="titles")
    fig_growth = px.area(
        content_growth,
        x="release_year",
        y="titles",
        color="type",
        markers=True,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"release_year": "Release Year", "titles": "Number of Titles", "type": "Content Type"},
    )
    fig_growth.update_traces(
        mode="lines+markers",
        hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Titles: %{y:,}<extra></extra>",
    )
    st.plotly_chart(apply_common_layout(fig_growth, height=500), use_container_width=True)


# -----------------------------------------------------------------------------
# Dataset preview
# -----------------------------------------------------------------------------
with st.expander("📋 Dataset Preview", expanded=False):
    st.caption(f"{format_number(len(filtered_df))} of {format_number(len(df))} records")
    st.dataframe(
        filtered_df[
            [
                "show_id",
                "type",
                "title",
                "director",
                "country",
                "date_added",
                "release_year",
                "rating",
                "duration",
                "listed_in",
                "description",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built with Streamlit, Pandas, and Plotly.
    </div>
    """,
    unsafe_allow_html=True,
)