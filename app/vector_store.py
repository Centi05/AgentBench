import uuid
from qdrant_client import QdrantClient, models
from app.chunker import Chunk

class VectorStore:
    def __init__(self, url: str, collection: str, dimension: int):
        self.client = QdrantClient(url=url)
        self.collection = collection
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE),
            )
        else:
            existing = self.client.get_collection(collection).config.params.vectors
            if existing.size != dimension:
                raise ValueError("Collection embedding dimension mismatch. Use a new collection name.")

    def upsert(self, chunks: list[Chunk], vectors):
        if len(chunks) != len(vectors):
            raise ValueError("Chunk/vector count mismatch")
        points = []
        for chunk, vector in zip(chunks, vectors):
            stable_key = f"{chunk.source}|{chunk.page_number}|{chunk.chunk_index}"
            points.append(models.PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, stable_key)),
                vector=vector.tolist(),
                payload={"source": chunk.source, "page_number": chunk.page_number,
                         "chunk_index": chunk.chunk_index, "text": chunk.text},
            ))
        for start in range(0, len(points), 100):
            self.client.upsert(collection_name=self.collection, points=points[start:start+100], wait=True)

    def search(self, vector, limit: int = 5):
        result = self.client.query_points(
            collection_name=self.collection, query=vector.tolist(), limit=limit, with_payload=True
        )
        return result.points
