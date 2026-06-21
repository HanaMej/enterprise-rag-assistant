from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

COLLECTION_NAME = "documents"

client = QdrantClient(path="qdrant_storage")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_collection_if_not_exists():
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_chunks(chunks: list[str], filename: str):
    create_collection_if_not_exists()

    points = []

    for index, chunk in enumerate(chunks):
        vector = embedding_model.encode(chunk).tolist()

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "filename": filename,
                    "chunk_index": index
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)

def search_chunks(query: str, limit: int = 5):
    create_collection_if_not_exists()

    query_vector = embedding_model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return [
        {
            "text": point.payload["text"],
            "filename": point.payload["filename"],
            "chunk_index": point.payload["chunk_index"],
            "score": point.score
        }
        for point in results.points
    ]

def list_documents():
    create_collection_if_not_exists()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True
    )

    filenames = sorted(
        set(point.payload["filename"] for point in points if point.payload)
    )

    return filenames


def clear_collection():
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME in collection_names:
        client.delete_collection(collection_name=COLLECTION_NAME)

    create_collection_if_not_exists()

    return True