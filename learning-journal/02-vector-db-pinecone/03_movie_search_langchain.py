import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# ============================================================
# STEP 1: Load model + Connect to Pinecone
# LangChain wraps the model — no need to call model.encode() manually
# ============================================================
print("STEP 1: Loading model and connecting to Pinecone...")

# LangChain handles the embedding — just pass the model name
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("✅ Model loaded!")
print("✅ Connected to Pinecone!")
input("\nPress Enter to go to STEP 2...\n")

# ============================================================
# STEP 2: Create Index
# ============================================================
print("STEP 2: Creating index...")

index_name = "movie-search-lc"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"✅ Index '{index_name}' created!")
else:
    print(f"✅ Index '{index_name}' already exists, skipping creation.")

input("\nPress Enter to go to STEP 3...\n")

# ============================================================
# STEP 3: Insert Movies
# LangChain uses Document objects — no manual vector building needed
# texts + metadatas is all you need, LangChain handles the rest
# ============================================================
print("STEP 3: Inserting movies...")

from langchain.schema import Document

movies = [
    Document(page_content="A thief enters people's dreams to steal secrets from their subconscious.",         metadata={"title": "Inception",       "genre": "Sci-Fi"}),
    Document(page_content="Batman fights the Joker, a criminal mastermind who wants chaos in Gotham.",       metadata={"title": "The Dark Knight",  "genre": "Action"}),
    Document(page_content="Astronauts travel through a wormhole in space to find a new home for humanity.",  metadata={"title": "Interstellar",     "genre": "Sci-Fi"}),
    Document(page_content="A poor young man falls in love with a rich girl and their love spans decades.",   metadata={"title": "The Notebook",     "genre": "Romance"}),
    Document(page_content="Superheroes unite to reverse the destruction caused by Thanos.",                  metadata={"title": "Avengers Endgame", "genre": "Action"}),
    Document(page_content="A love story between two people from different classes aboard the Titanic.",      metadata={"title": "Titanic",          "genre": "Romance"}),
    Document(page_content="A hacker discovers the world is a simulation and joins a rebellion.",             metadata={"title": "The Matrix",       "genre": "Sci-Fi"}),
    Document(page_content="A simple kind-hearted man unintentionally influences major historical events.",   metadata={"title": "Forrest Gump",     "genre": "Drama"}),
    Document(page_content="A poor family schemes their way into working for a wealthy family.",              metadata={"title": "Parasite",         "genre": "Thriller"}),
    Document(page_content="A young lion prince must reclaim his kingdom after his father's murder.",         metadata={"title": "The Lion King",    "genre": "Animation"}),
]

# One line to embed + insert all documents into Pinecone
vectorstore = PineconeVectorStore.from_documents(movies, embeddings, index_name=index_name)

print("✅ All movies inserted!")
input("\nPress Enter to go to STEP 4...\n")

# ============================================================
# STEP 4: Search
# LangChain gives you similarity_search() — no manual query vector needed
# ============================================================
while True:
    print("\nSTEP 4: Movie Search")
    print("-" * 40)
    query = input("Describe what kind of movie you want (or 'quit' to exit): ")

    if query.lower() == "quit":
        break

    # One line to search — LangChain handles embedding the query
    results = vectorstore.similarity_search_with_score(query, k=3)

    print(f"\nTop 3 movies for: '{query}'")
    print("-" * 40)
    for i, (doc, score) in enumerate(results, 1):
        print(f"{i}. {doc.metadata['title']} ({doc.metadata['genre']}) — Score: {score:.2f}")
        print(f"   Plot: {doc.page_content}")

print("\n✅ Done!")
