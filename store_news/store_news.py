import json
from google.cloud import firestore

def store_news(event, context):
    """Triggered by a message on a Cloud Pub/Sub topic."""
    client = firestore.Client()
    
    # Decode and parse the Pub/Sub message
    pubsub_message = event['data']
    article = json.loads(pubsub_message.decode('utf-8'))
    
    # Add the article to Firestore
    doc_ref = client.collection('news_articles').add(article)
    
    print(f'Article added with ID: {doc_ref.id}')
