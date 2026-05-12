import os
from ingest import ingest_pdfs
from retrieval import retrieve_docs
from generator import generate_answer
from hitl import human_fallback
from graph import build_graph

def main():
    print(" Checking knowledge base...")
    pdfs = ["PDFs/kb.pdf"]  # add your PDF paths here

    if not os.path.exists("db"):
        ingest_pdfs(pdfs)
    else:
        print("Using existing vector database")

    graph = build_graph()
    print(" System Ready!")

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break

        state = {
            "query": query,
            "retriever": retrieve_docs,
            "generator": generate_answer,
            "hitl": human_fallback,
            "answer": "",
            "escalate": False
        }

        result = graph.invoke(state)
        print("\nFinal Answer:")
        print(result["answer"])

if __name__ == "__main__":
    main()
