import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "vector.index"
METADATA_PATH = "metadata.pkl"

dimension = 384

if os.path.exists(INDEX_PATH):

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)

else:

    index = faiss.IndexFlatL2(dimension)

    metadata_store = []


def store_finding(
    embedding,
    metadata
):

    vector = np.array(
        [embedding],
        dtype="float32"
    )

    index.add(vector)

    metadata_store.append(metadata)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata_store, f)


def search_similar(
    embedding,
    top_k=5
):

    if index.ntotal == 0:
        return []

    vector = np.array(
    [embedding],
    dtype="float32"
)
    distances, indices = index.search(
        vector,
        top_k
    )

    print("Total vectors:", index.ntotal)
    print("Metadata count:", len(metadata_store))

    results = []

    for idx in indices[0]:

        if idx < len(metadata_store):

            results.append(
                metadata_store[idx]
            )

    return results