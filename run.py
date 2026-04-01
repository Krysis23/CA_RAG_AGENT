from search import search_rag
from ca_agent import process_query
from file_handler import extract_text
import os

user_text = input("Enter your query (or press enter): ")
file_path = input("Enter file path (optional): ")

file_text = ""

if file_path.strip() != "" and os.path.exists(file_path):
    file_text = extract_text(file_path)

    print("\n----- Extracted File Text -----\n")
    print(file_text)

final_query = (user_text + " " + file_text).strip()
final_query = final_query.replace("\n", " ")

print("\n----- Final Query -----\n")
print(final_query)


chunks = search_rag(final_query, top_k=3)


level_order = {
    "final": 0,
    "intermediate": 1,
    "foundation": 2
}

if "level" in chunks.columns:
    chunks = chunks.sort_values(
        by="level",
        key=lambda col: col.map(level_order)
    )


print("\n----- Retrieved Chunks -----")
print(chunks[["level", "book", "chunk_id"]])

retrieved_context = chunks.to_json(orient="records")

answer = process_query(final_query, retrieved_context)

print("\n----- Answer -----\n")
print(answer)


