from semantic_search import search_papers


results = search_papers("deep learning", limit=5)

for i, paper in enumerate(results, start=1):
    print(f"{i}. {paper['title']} ({paper['year']})")
print("Results received:", results)
