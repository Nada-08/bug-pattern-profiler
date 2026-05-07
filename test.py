from packages.retrieval.vector_store import PineconeVectorStore

store = PineconeVectorStore()

# store.delete_namespace("__default__")

print(store.index.describe_index_stats())