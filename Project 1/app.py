import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("combined_movie_dataset.csv")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Clean column names
df.columns = df.columns.str.strip()

# Check for required columns
required_columns = {"title", "genres", "actors", "rating"}
if not required_columns.issubset(df.columns):
    st.error(f"❌ Dataset must contain columns: {required_columns}")
    st.stop()

# Drop missing essential data
df = df.dropna(subset=["title", "genres", "actors", "rating"])

# Convert genres and actors into lists
df["genres"] = df["genres"].apply(lambda x: [g.strip() for g in str(x).split("|")])
df["actors"] = df["actors"].apply(lambda x: [a.strip() for a in str(x).split(",")])

# Get unique genres and actors for selection
all_genres = sorted(set(g for genres in df["genres"] for g in genres))
all_actors = sorted(set(a for actors in df["actors"] for a in actors))

# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_genres = st.multiselect("Select Genre(s)", all_genres)
selected_actors = st.multiselect("Select Actor(s)", all_actors)
min_rating = st.slider("Minimum Rating", 0.5, 5.0, 3.0, step=0.5)

# Filter logic
def movie_matches(row):
    has_genre = all(g in row["genres"] for g in selected_genres) if selected_genres else True
    has_actor = any(a in row["actors"] for a in selected_actors) if selected_actors else True
    meets_rating = row["rating"] >= min_rating
    return has_genre and has_actor and meets_rating

filtered_df = df[df.apply(movie_matches, axis=1)]

# Display results
st.subheader("🎥 Recommended Movies")
if not filtered_df.empty:
    for _, row in filtered_df.sort_values(by="rating", ascending=False).head(10).iterrows():
        st.markdown(f"**{row['title']}** — ⭐ {row['rating']:.1f}  \n*Actors:* {', '.join(row['actors'])}  \n*Genres:* {', '.join(row['genres'])}")
else:
    st.warning("No movies found. Try selecting different filters.")
