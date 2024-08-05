import json
import base64
from google.cloud import firestore
from google.cloud import pubsub_v1

def summarize_news(event, context):
    # Initialize Firestore client
    db = firestore.Client()

    # Decode and parse the Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    article = json.loads(pubsub_message)

    # Extract the article content and metadata
    article_id = article.get('id')
    article_content = article.get('content')
    
    # Perform text summarization (replace this with your actual summarization code)
    summary = summarize_text(article_content)

    # Prepare the document to be saved in Firestore
    document = {
        'original_content': article_content,
        'summary': summary
    }

    # Save the document to Firestore
    doc_ref = db.collection('summarized_articles').document(article_id)
    doc_ref.set(document)

    print(f'Successfully processed and summarized article ID: {article_id}')

def summarize_text(text):
    # Placeholder for text summarization logic
    # Replace this with actual summarization code or API call
    return text[:100] + '...'  # Example: truncate text for summary
