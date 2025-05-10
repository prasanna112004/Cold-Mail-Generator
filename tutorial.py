# %%
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="test_collection")
# %%
collection.add(
    documents=[
        "This document is about Mumbai indians",
        "This document is about Royal challengers banglore"
    ],
    ids = ['id1','id2']
)

documents = collection.get(ids=["id2"])
print(documents)

# %%
results = collection.query(
    query_texts=["Query is about Virat"],
    n_results = 2
)
print(results)
# %%
