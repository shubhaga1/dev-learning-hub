import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# ============================================================
# STEP 1: Load model + Connect to Pinecone
# ============================================================
print("STEP 1: Loading model and connecting to Pinecone...")

model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("✅ Model loaded!")
print("✅ Connected to Pinecone!")
input("\nPress Enter to go to STEP 2...\n")

# ============================================================
# STEP 2: Create Index
# ============================================================
print("STEP 2: Creating index...")

index_name = "movie-search"

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

index = pc.Index(index_name)
input("\nPress Enter to go to STEP 3...\n")

# ============================================================
# STEP 3: Insert Movies
# ============================================================
print("STEP 3: Inserting movies into Pinecone...")

movies = [
    {"id": "1", "title": "Inception",         "genre": "Sci-Fi",   "plot": "A thief enters people's dreams to steal secrets from their subconscious."},
    {"id": "2", "title": "The Dark Knight",    "genre": "Action",   "plot": "Batman fights the Joker, a criminal mastermind who wants to create chaos in Gotham."},
    {"id": "3", "title": "Interstellar",       "genre": "Sci-Fi",   "plot": "Astronauts travel through a wormhole in space to find a new home for humanity."},
    {"id": "4", "title": "The Notebook",       "genre": "Romance",  "plot": "A poor young man falls in love with a rich girl and their love story spans decades."},
    {"id": "5", "title": "Avengers Endgame",   "genre": "Action",   "plot": "Superheroes unite to reverse the destruction caused by Thanos and restore the universe."},
    {"id": "6", "title": "Titanic",            "genre": "Romance",  "plot": "A love story between two people from different classes aboard the ill-fated Titanic ship."},
    {"id": "7", "title": "The Matrix",         "genre": "Sci-Fi",   "plot": "A hacker discovers the world is a simulation and joins a rebellion against machines."},
    {"id": "8", "title": "Forrest Gump",       "genre": "Drama",    "plot": "A simple man with a kind heart unintentionally influences major historical events in America."},
    {"id": "9", "title": "Parasite",           "genre": "Thriller", "plot": "A poor family schemes their way into working for a wealthy family with dark consequences."},
    {"id": "10","title": "The Lion King",      "genre": "Animation","plot": "A young lion prince flees his kingdom after his father's murder and must reclaim his throne."},
]

vectors = []
for movie in movies:
    # We embed the plot so search finds movies by meaning of the story
    embedding = model.encode(movie["plot"]).tolist()
    vectors.append({
        "id": movie["id"],
        "values": embedding,
        "metadata": {
            "title": movie["title"],
            "genre": movie["genre"],
            "plot": movie["plot"]
        }
    })
    print(f"  → {movie['title']} ({movie['genre']})")

index.upsert(vectors=vectors)
print("\n✅ All movies inserted!")
input("\nPress Enter to go to STEP 4...\n")

# ============================================================
# STEP 4: Search Movies
# ============================================================
while True:
    print("\nSTEP 4: Movie Search")
    print("-" * 40)
    query = input("Describe what kind of movie you want (or 'quit' to exit): ")

    if query.lower() == "quit":
        break

    query_vector = model.encode(query).tolist()

    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    print(f"\nTop 3 movies for: '{query}'")
    print("-" * 40)
    for i, match in enumerate(results["matches"], 1):
        m = match["metadata"]
        print(f"{i}. {m['title']} ({m['genre']}) — Score: {match['score']:.2f}")
        print(f"   Plot: {m['plot']}")

print("\n✅ Done!")
