import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "soft_corner_docs"
JSON_PATH = "data/soft_corner_rag_corpus.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

client = QdrantClient(url=QDRANT_URL)

sample_vector = model.encode("test").tolist()
vector_size = len(sample_vector)

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    ),
)

points = []

for idx, item in enumerate(data):
    vector = model.encode(item["page_content"]).tolist()

    points.append(
        models.PointStruct(
            id=idx,
            vector=vector,
            payload=item
        )
    )

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("✅ Local embedding + upload done")