from gef_analyzr.search.occurrence_search import OccurrenceSearcher

if __name__ == "__main__":
    searcher = OccurrenceSearcher(issue="How is air pollution mentioned?", threshold=10)
    results = searcher.getUniqueDocumentOccurrences()
    [print(f"'{result}'\n\n") for result in results]

    documents = set()
    for result in results:
        documents.add(result.payload.get('file_path'))

    print(f'Documents with Occurrences:\n{documents}')
