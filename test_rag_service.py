from packages.rag.rag_service import RAGService


rag = RAGService()

result = rag.answer(
    query="What are common patterns in authentication bypass vulnerabilities?",
    top_k=5,
    namespace="fused"
)

print("ANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print("-", source["cve_id"], "|", source["title"])