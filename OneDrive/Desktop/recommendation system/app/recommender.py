import ast
import os
import numpy as np

from dotenv import load_dotenv
from supabase import create_client
from sklearn.neighbors import NearestNeighbors

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def load_product_embeddings():

    rows = (
        supabase
        .table("embeddings")
        .select("*")
        .execute()
        .data
    )

    product_ids = []
    vectors = []

    for row in rows:

        if row["embedding"] is None:
            continue

        product_ids.append(row["product_id"])

        embedding = row["embedding"]

        if isinstance(embedding, str):
            embedding = ast.literal_eval(embedding)

        vectors.append(embedding)

    return product_ids, np.array(vectors)


def load_trend_embeddings():

    rows = (
        supabase
        .table("trend_embeddings")
        .select("*")
        .execute()
        .data
    )

    return rows


def save_recommendations(
    trend_id,
    product_ids,
    similarities
):

    for product_id, score in zip(
        product_ids,
        similarities
    ):

        supabase.table(
            "recommendations"
        ).insert({
            "trend_id": trend_id,
            "product_id": int(product_id),
            "similarity_score": float(score)
        }).execute()


def run():



    print("Loading product embeddings...")

    product_ids, product_vectors = (
        load_product_embeddings()
    )

    print(
        f"Loaded {len(product_vectors)} products"
    )

    print("Product vectors shape:")
    print(product_vectors.shape)

    print("First vector length:")
    print(len(product_vectors[0]))

    knn = NearestNeighbors(
        n_neighbors=5,
        metric="cosine"
    )

    knn.fit(product_vectors)

    trends = load_trend_embeddings()

    print(
        f"Loaded {len(trends)} trends"
    )

    for trend in trends:

        embedding = trend["embedding"]

        if isinstance(embedding, str):
            embedding = ast.literal_eval(embedding)

        trend_vector = np.array(
            embedding,
            dtype=np.float32
        ).reshape(1, -1)

        print("Trend vector shape:")
        print(trend_vector.shape)

        distances, indices = knn.kneighbors(
            trend_vector
        )

        nearest_products = [
            product_ids[i]
            for i in indices[0]
        ]

        similarities = [
            1 - d
            for d in distances[0]
        ]

        save_recommendations(
            trend["trend_id"],
            nearest_products,
            similarities
        )

        print(
            f"Trend {trend['trend_id']} -> saved 5 recommendations"
        )


if __name__ == "__main__":
    run()