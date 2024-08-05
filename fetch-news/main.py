import os
import requests
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GCP_PROJECT = os.getenv('GCP_PROJECT')
TOPIC_ID = 'news-articles'

def fetch_and_publish_news(request):
    # Define the NewsAPI endpoint
    NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

    # Fetch news articles
    response = requests.get(NEWS_API_URL)
    if response.status_code != 200:
        return f'Failed to fetch news articles: {response.status_code}', 500
    
    articles = response.json().get('articles', [])

    # Initialize the Pub/Sub client
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT, TOPIC_ID)
    
    # Publish articles to Pub/Sub
    for article in articles:
        article_data = {
            'title': article.get('title'),
            'description': article.get('description'),
            'url': article.get('url'),
            'content': article.get('content')
        }
        publisher.publish(topic_path, data=str(article_data).encode('utf-8'))

    return f'Published {len(articles)} articles to Pub/Sub', 200
