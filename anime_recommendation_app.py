import streamlit as st
import random
import requests

# Anime-inspired quotes
anime_quotes = [
    "“It's not the face that makes someone a monster; it's the choices they make with their lives.” - Naruto Uzumaki",
    "“A lesson without pain is meaningless.” - Edward Elric, Fullmetal Alchemist",
    "“The world isn’t perfect, but it’s there for us, doing the best it can… that’s what makes it so damn beautiful.” - Roy Mustang",
    "“I don’t care what the world thinks of me, I just want to fight alongside my friends.” - Natsu Dragneel, Fairy Tail"
]

# Fun message or anime quote
def display_fun_message():
    quote = random.choice(anime_quotes)
    st.markdown(f"**{quote}**")

# Cache for recommendations to speed up loading
@st.cache_data
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

# Fetch random anime
@st.cache_data
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

# Main app
def main():
    # Setting page with custom theme
    st.set_page_config(page_title="AnimeQuest: Your Anime Adventure", page_icon="🎥", layout="wide")
    
    # Fun header with emojis
    st.title("🌟 Welcome to AnimeQuest! 🌟")
    
    # Display a random anime quote
    display_fun_message()
    
    # Option for user to input anime
    user_input = st.text_input("Enter an anime you've watched:", placeholder="e.g., Naruto, Attack on Titan")
    
    # Add an anime recommendation button with a friendly style
    if st.button("Get Anime Recommendations 👑"):
        if user_input:
            recommendations = get_anime_recommendations(user_input)
            if recommendations:
                st.subheader("Anime Recommendations For You ✨:")
                for anime in recommendations:
                    st.image(anime['image_url'], width=150)  # Resize image width for quicker loading
                    st.write(f"**{anime['title']}**")
            else:
                st.warning("Oops! No recommendations found 😓")
        else:
            st.warning("Please enter an anime name to get started! 🙏")
    
    # Display random anime with a fun twist
    st.subheader("✨ Random Anime ✨")
    random_anime = get_random_anime()
    if random_anime:
        st.image(random_anime['image_url'], width=150)
        st.write(f"**{random_anime['title']}**")
        st.write(f"Synopsis: {random_anime['synopsis']}")
        st.write(f"Score: {random_anime['score']} 🏅")
        st.write(f"Episodes: {random_anime['episodes']}")
        st.write(f"Type: {random_anime['type']}")
    else:
        st.warning("Could not fetch random anime 😢")
    
    # Fun footer message
    st.markdown("---")
    st.markdown("**Join the Anime Quest** 💫 | Explore, discover, and watch the best anime recommendations in the universe!")

if __name__ == "__main__":
    main()
