import streamlit as st
import requests

# Function to fetch Hacker News stories
def fetch_hacker_news_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    top_story_ids = response.json()[:10]  # Get the top 10 story IDs
    stories = []

    for story_id in top_story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
        story_response = requests.get(story_url)
        story = story_response.json()
        stories.append(story)

    return stories

# Streamlit app
def main():
    st.title("Hacker News Top Stories")
    st.markdown("This app displays the top stories from Hacker News.")

    stories = fetch_hacker_news_stories()

    for story in stories:
        st.write(f"**Title:** [{story['title']}]({story['url']})")
        st.write(f"**Author:** {story['by']}")
        st.write(f"**Score:** {story['score']}")
        st.write(f"**Comments:** {story['descendants']}")
        st.write("---")

if __name__ == "__main__":
    main()

