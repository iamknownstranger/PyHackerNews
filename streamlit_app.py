import nltk
nltk.download('all')

import os

import openai
import requests
import streamlit as st
from newspaper import Article

# TODO: Add summary and description to the story

if "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
   openai.api_key = st.secrets['OPENAI_API_KEY']

# Function to fetch Hacker News stories through the official API
def fetch_hacker_news_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    top_story_ids = response.json()[:5]
    return top_story_ids


@st.cache_data()
def get_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    story = response.json()

    article = Article(story["url"])

    # Download and parse the article
    article.download()
    article.parse()

    # Perform natural language processing on the article
    article.nlp()

    # Print the article title
    story["title"] = article.title

    # Geneate summary of the article using GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": f"You're a great research article writer! and very skillful in summarizing articles. I have a task for you."},
            {"role": "user", "content": f"summarize the followning article briefly and use markdown formatting wherever needed like code snippets with headers less than two stars: {article.text}"},
        ],
    )
    summary = response["choices"][0]["message"]["content"]
    story["summary"] = summary

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
            st.write(f"*Author:* {story['by']}")
            st.write(f"**Summary:** {story['summary']}")
            st.write("---")


if __name__ == "__main__":
    main()
