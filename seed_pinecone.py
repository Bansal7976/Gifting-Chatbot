import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from data import products_for_ordering
import time

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PINECONE_INDEX_NAME = "gifting-chatbot"

def main():
    """Main function to run the seeding process."""
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Create index if it doesn't exist
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,  # Dimension for "models/embedding-001"
            metric="cosine", 
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
            print("Waiting for index to be ready...")
            time.sleep(5)
        print("Index created successfully.")
    else:
        print(f"Index '{PINECONE_INDEX_NAME}' already exists.")

    index = pc.Index(PINECONE_INDEX_NAME)
    
    print("Preparing data and generating embeddings...")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
    
    all_products = []
    for category, items in products_for_ordering.items():
        for name, details in items.items():
            text_to_embed = (
                f"Gift ka naam: {name}. Description: {details['description']}. "
                f"Yeh {category} category mein aata hai. Iski keemat {details['price']} rupees hai."
            )
            all_products.append({
                'id': name.replace(" ", "-").lower(),
                'text': text_to_embed,
                'metadata': {'product_name': name, 'category': category, 'price': details['price'], 'description': details['description']}
            })

    texts = [p['text'] for p in all_products]
    embeddings = embeddings_model.embed_documents(texts)

    vectors_to_upload = []
    for i, product in enumerate(all_products):
        vectors_to_upload.append({
            'id': product['id'],
            'values': embeddings[i],
            'metadata': product['metadata']
        })

    print(f"Generated embeddings for {len(all_products)} products.")
    
    print("Uploading vectors to Pinecone...")
    batch_size = 100
    for i in range(0, len(vectors_to_upload), batch_size):
        batch = vectors_to_upload[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"Uploaded batch {i//batch_size + 1}")
    
    print("All vectors uploaded successfully!")

if __name__ == "__main__":
    main()