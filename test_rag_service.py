from packages.rag.rag_service import RAGService

rag = RAGService()

queries = [
    # "What is CVE-2021-44228?",
    "Show critical Microsoft vulnerabilities"
]

for i, query in enumerate(queries, 1):
    print("=" * 100)
    print(f"TEST {i}")
    print(query)
    print("=" * 100)

    result = rag.answer(
        query=query,
        top_k=5,
        namespace="fused",
    )

    print("\nSources:")
    for src in result["sources"]:
        print(
            f"- {src.cve_id} | {src.title} | score={src.score:.3f}" 
        )

    print("\nAnswer:")
    print(result["answer"])
    print("\n")