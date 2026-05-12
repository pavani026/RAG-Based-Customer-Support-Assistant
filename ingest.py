from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def ingest_pdfs(pdf_list):
    try:
        all_docs = []
        for pdf_path in pdf_list:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            for doc in documents:
                doc.metadata["source"] = pdf_path
            all_docs.extend(documents)
        print(f" Loaded {len(all_docs)} pages")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(all_docs)
        print(f"Created {len(chunks)} chunks")

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        vectorstore = Chroma(
            persist_directory="db",
            embedding_function=embeddings
        )
        vectorstore.add_documents(chunks)
        vectorstore.persist()
        print(" All PDFs processed and stored successfully")

    except Exception as e:
        print(" Ingestion Error:", e)
