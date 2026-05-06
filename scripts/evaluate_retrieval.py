from packages.retrieval.search_service import SearchService

evaluation_queries = [
    {
        "query": "authentication bypass vulnerabilities",
        "expected_terms": ["authentication", "bypass", "CWE-287"],
    },
    {
        "query": "remote code execution vulnerabilities",
        "expected_terms": ["remote code execution", "RCE", "code execution"],
    },
    {
        "query": "privilege escalation vulnerabilities",
        "expected_terms": ["privilege", "escalation", "CWE-269"],
    },
    {
        "query": "path traversal file access vulnerabilities",
        "expected_terms": ["path traversal", "directory traversal", "CWE-22"],
    },
    {
        "query": "network attack vector critical vulnerabilities",
        "expected_terms": ["NETWORK", "CRITICAL"],
    },
]

search = SearchService()

for item in evaluation_queries:
    query = item["query"]
    expected_terms = item["expected_terms"]

    print("=" * 80)
    print(f"QUERY: {query}")
    print(f"EXPECTED TERMS: {expected_terms}")
    print("-" * 80)

    results = search.search(query, top_k=5)

    for i, result in enumerate(results, start=1):
        metadata = result
        text = result.get("text", "")

        print(f"CVE: {result.get('cve_id')}")
        print(f"Title: {result.get('title')}")
        print(f"Severity: {result.get('severity')}")
        print(f"CWE: {result.get('cwe_ids')}")
        print(f"Text Preview: {text[:400]}")