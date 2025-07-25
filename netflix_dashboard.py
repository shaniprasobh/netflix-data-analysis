# netflix_dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(layout="wide", page_title="Netflix Data Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

st.title("📺 Netflix Movies and TV Shows Dashboard")

# Sidebar filters
st.sidebar.header("🎛️ Filters")
type_options = st.sidebar.multiselect("Select Type", df['type'].dropna().unique(), default=df['type'].dropna().unique())
country_options = st.sidebar.multiselect("Select Country", df['country'].dropna().unique()[:20], default=None)
year_range = st.sidebar.slider("Select Year Range", int(df['year_added'].min() or 2008), int(df['year_added'].max() or 2025), (2010, 2020))

# Apply filters
filtered_df = df[df['type'].isin(type_options)]
if country_options:
    filtered_df = filtered_df[filtered_df['country'].isin(country_options)]
filtered_df = filtered_df[filtered_df['year_added'].between(*year_range)]

st.markdown(f"### Showing {len(filtered_df)} records")

# --- Plot 1: Content Added per Year
st.subheader("📅 Content Added per Year")
yearly_counts = filtered_df['year_added'].value_counts().sort_index()

fig1, ax1 = plt.subplots()
sns.barplot(x=yearly_counts.index, y=yearly_counts.values, ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Titles")
ax1.set_title("Content Added to Netflix per Year")
st.pyplot(fig1)

# --- Plot 2: Movie vs TV Show Trend
st.subheader("🎬 Movies vs TV Shows Over the Years")
trend_data = filtered_df.groupby(['year_added', 'type']).size().unstack().fillna(0)
fig2, ax2 = plt.subplots()
trend_data.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Titles")
ax2.set_title("Movie vs TV Show Trend")
st.pyplot(fig2)

# --- Plot 3: Top Countries
st.subheader("🌍 Top 10 Content-Producing Countries")
top_countries = filtered_df['country'].value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(y=top_countries.index, x=top_countries.values, ax=ax3)
ax3.set_title("Top 10 Countries by Number of Titles")
ax3.set_xlabel("Number of Titles")
st.pyplot(fig3)

# --- Plot 4: Top Genres
st.subheader("🎭 Top 10 Genres")
genres = filtered_df['listed_in'].dropna().str.split(', ')
flat_genres = [g for sublist in genres for g in sublist]
top_genres = Counter(flat_genres).most_common(10)
genre_labels, genre_counts = zip(*top_genres)
fig4, ax4 = plt.subplots()
sns.barplot(x=genre_counts, y=genre_labels, ax=ax4)
ax4.set_title("Top 10 Genres on Netflix")
st.pyplot(fig4)
