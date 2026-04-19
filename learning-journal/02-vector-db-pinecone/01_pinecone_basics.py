import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

print(os.path.dirname(__file__))
print(os.path)
# ============================================================
# STEP 1: Load the embedding model + Connect to Pinecone
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

index_name = "demo-index"

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
# STEP 3: Insert Data
# ============================================================
print("STEP 3: Converting text to vectors and inserting into Pinecone...")

sentences = [
    {"id": "1", "text": "shubham is a software engineer"},
    {"id": "2", "text": "rahul is a product manager"},
    {"id": "3", "text": "priya is a UI designer"},
    {"id": "4", "text": "coding and programming is fun"},
    {"id": "5", "text": "design and creativity go hand in hand"},
]

vectors = []
for item in sentences:
    embedding = model.encode(item["text"]).tolist()
    vectors.append({
        "id": item["id"],
        "values": embedding,
        "metadata": {"text": item["text"]}
    })
    print(f"  → '{item['text']}' converted to vector of {len(embedding)} numbers")

index.upsert(vectors=vectors)
print("\n✅ All data inserted into Pinecone!")
input("\nPress Enter to go to STEP 4...\n")

# ============================================================
# STEP 4: Search
# ============================================================
print("STEP 4: Searching...")

query = input("Enter your search query: ")
query_vector = model.encode(query).tolist()

results = index.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True
)

print(f"\nTop 3 matches for: '{query}'")
print("-" * 40)
for i, match in enumerate(results["matches"], 1):
    print(f"{i}. Score: {match['score']:.2f} | {match['metadata']['text']}")

print("\n✅ Done!")
