import nltk
nltk.download('punkt')

import streamlit as st
import requests

# TODO: Add summary and description to the story

# # Import the library
from newspaper import Article


# Function to fetch Hacker News stories
def fetch_hacker_news_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    top_story_ids = response.json()    
    return top_story_ids

def get_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    story = response.json()
    # st.write(f"**Title:** [{story['title']}]({story['url']})")

    article = Article(story["url"])

    # Download and parse the article
    article.download()
    article.parse()

    # Perform natural language processing on the article
    article.nlp()

    # Print the article title
    story["TITLE"] = article.title

    # Print the article summary
    story["SUMMARY"] = article.summary

    return story

# Streamlit app
def main():
    st.title("Hacker News Top Stories")
    st.markdown("This app displays the top stories from Hacker News.")

    stories = fetch_hacker_news_stories()

    for story_id in stories:
        with st.container():
            story = get_story(story_id)
            st.subheader(f"[{story['title']}]({story['url']})")
            st.write(f"**Author:** {story['by']}")
            st.write(f"**Score:** {story['score']}")
            st.write(f"**Comments:** {story['descendants']}")
            st.write(f"**Summary:** {story['SUMMARY']}")
            st.write("---")
if __name__ == "__main__":
    main()

