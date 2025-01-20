import streamlit as st
import random
import requests

# Function to fetch anime recommendations
def get_anime_recommendations(input_anime):
    url = f"https://api.jikan.moe/v4/anime?q={input_anime}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            anime_id = data["data"][0]["mal_id"]
            recommendations_url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
            recommendations_response = requests.get(recommendations_url)

            if recommendations_response.status_code == 200:
                recommendations_data = recommendations_response.json()
                if recommendations_data["data"]:
                    return [
                        {
                            "title": rec["entry"]["title"],
                            "image_url": rec["entry"]["images"]["jpg"]["image_url"]
                        }
                        for rec in recommendations_data["data"]
                    ]
    return []

# Function to fetch a random anime
def get_random_anime():
    random_page = random.randint(1, 100)
    url = f"https://api.jikan.moe/v4/anime?page={random_page}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            anime = data["data"][0]
            return {
                "title": anime["title"],
                "image_url": anime["images"]["jpg"]["image_url"],
                "synopsis": anime.get("synopsis", "Synopsis not available."),
                "score": anime.get("score", "N/A"),
                "episodes": anime.get("episodes", "Unknown"),
                "type": anime.get("type", "Unknown")
            }
    return None

# Function to fetch top anime of the season
def get_top_season_anime():
    url = "https://api.jikan.moe/v4/seasons/now"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "title": anime["title"],
                "image_url": anime["images"]["jpg"]["image_url"]
            }
            for anime in data["data"]
        ]
    return []

# Function to fetch anime by genre
def get_anime_by_genre(genre):
    url = f"https://api.jikan.moe/v4/anime?genres={genre}&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "title": anime["title"],
                "image_url": anime["images"]["jpg"]["image_url"]
            }
            for anime in data["data"]
        ]
    return []

# Main function
def main():
    # Set page configuration
    st.set_page_config(page_title="AnimeQuest: Your Anime Adventure", page_icon="🎥", layout="wide")

    # Apply custom CSS for styling
    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f6f9;
        overflow-x: hidden;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.2s;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextInput input {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
    }
    img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin-bottom: 10px;
        transition: transform 0.2s ease-in-out;
    }
    img:hover {
        transform: scale(1.05);
    }
    .anime-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease;
    }
    .anime-card:hover {
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    }
    .anime-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        text-align: center;
        text-decoration: none;
    }
    .anime-title:hover {
        color: #4CAF50;
        text-decoration: underline;
    }
    .container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
        padding: 20px;
    }
    .header {
        text-align: center;
        font-size: 40px;
        color: #4CAF50;
        font-weight: bold;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes glow {
        0% {
            text-shadow: 0 0 5px #4CAF50, 0 0 10px #4CAF50, 0 0 15px #4CAF50;
        }
        100% {
            text-shadow: 0 0 15px #4CAF50, 0 0 30px #4CAF50, 0 0 45px #4CAF50;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title and description with glowing effect
    st.markdown("<h1 class='header'>AnimeQuest: Your Anime Adventure</h1>", unsafe_allow_html=True)
    st.write("Discover your next favorite anime with our recommendations, top season picks, and random suggestions!")

    # Input from user for anime recommendations
    user_input = st.text_input("Enter an anime you've watched:", placeholder="e.g., Naruto, Attack on Titan")

    # Fetch recommendations based on user input
    if st.button("Get Recommendations"):
        if user_input:
            recommendations = get_anime_recommendations(user_input)
            if recommendations:
                st.subheader("📌 Recommended Anime:")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<div class='container'>", unsafe_allow_html=True)
                for anime in recommendations:
                    st.markdown(
                        f"<div class='anime-card'><img src='{anime['image_url']}' alt='{anime['title']}'/><p class='anime-title'>{anime['title']}</p></div>",
                        unsafe_allow_html=True
                    )
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No recommendations found for the given anime.")
        else:
            st.warning("Please enter an anime to get recommendations.")

    # Random anime section
    st.markdown("### 🎲 Random Anime Recommendation")
    if st.button("Get a Random Anime"):
        random_anime = get_random_anime()
        if random_anime:
            st.markdown(
                f"<div class='anime-card'><img src='{random_anime['image_url']}' alt='{random_anime['title']}'/><p class='anime-title'>{random_anime['title']}</p><p>{random_anime['synopsis']}</p><p><strong>Type:</strong> {random_anime['type']}</p><p><strong>Episodes:</strong> {random_anime['episodes']}</p><p><strong>Score:</strong> {random_anime['score']}</p></div>",
                unsafe_allow_html=True
            )
        else:
            st.warning("Failed to fetch a random anime. Please try again.")

    # Top anime of the season
    st.markdown("### 🌟 Top Anime of the Season")
    if st.button("Get Top Anime"):
        top_anime = get_top_season_anime()
        if top_anime:
            st.subheader("Season's Best Picks:")
            st.markdown("<div class='container'>", unsafe_allow_html=True)
            for anime in top_anime:
                st.markdown(
                    f"<div class='anime-card'><img src='{anime['image_url']}' alt='{anime['title']}'/><p class='anime-title'>{anime['title']}</p></div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Failed to fetch top anime for this season.")

    # Anime genres filter
    st.markdown("### 🔍 Find Anime by Genre")
    genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Romance"]
    genre_choice = st.selectbox("Choose a Genre:", genres)

    if st.button("Get Anime by Genre"):
        genre_animes = get_anime_by_genre(genre_choice)
        if genre_animes:
            st.subheader(f"Anime Recommendations for {genre_choice} Genre:")
            st.markdown("<div class='container'>", unsafe_allow_html=True)
            for anime in genre_animes:
                st.markdown(
                    f"<div class='anime-card'><img src='{anime['image_url']}' alt='{anime['title']}'/><p class='anime-title'>{anime['title']}</p></div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning(f"No anime found for {genre_choice} genre.")

    # Fun anime fact section
    st.markdown("### 💡 Anime Fun Fact")
    fun_facts = [
        "Did you know? The longest-running anime is *Sazae-san* with over 7,000 episodes!",
        "Anime has been around since the early 20th century, with *Namakura Gatana* (1917) being one of the first.",
        "The word 'anime' is derived from the English word 'animation', but it refers specifically to Japanese animation."
    ]
    st.markdown(random.choice(fun_facts))

    # Disclaimer
    st.markdown("---")
    st.markdown(
        "**Disclaimer:** Data sourced from [Jikan API](https://jikan.moe). All rights reserved by their respective owners."
    )

if __name__ == "__main__":
    main()
