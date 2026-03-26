from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import json
import pickle
import pathlib

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
CHUNKS_DB_PATH = str(BASE_DIR / "chunks_db.pkl")
KNOWLEDGE_BASE_PATH = str(BASE_DIR / "knowledge_base")


def load_documents():
    """Load documents from the knowledge base directory."""
    documents = []
    for filename in os.listdir(KNOWLEDGE_BASE_PATH):
        filepath = os.path.join(KNOWLEDGE_BASE_PATH, filename)
        if filename.endswith(".txt"):
            if filename.endswith(".txt"):
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                documents.extend(docs)
                print(f"Loaded document: {filename} with {len(docs)} pages.")
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                documents.extend(docs)
            print(f"📄 Loaded document: {filename} with {len(docs)} pages.")
    return documents


def build_vector_store():
    """Build and save chunks from documents"""
    print("🔍 Building knowledge base...")

    # Load documents
    documents = load_documents()

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks.")

    chunk_texts = [chunk.page_content for chunk in chunks]

    # Save chunks to disk as pickle
    with open(CHUNKS_DB_PATH, "wb") as f:
        pickle.dump(chunk_texts, f)

    print(f"✅ Knowledge base built and saved with {len(chunks)} chunks.")
    return chunk_texts


# Load saved chunks from disk.
def load_chunks():
    """Load saved chunks from disk."""
    with open(CHUNKS_DB_PATH, "rb") as f:
        return pickle.load(f)


# Load search based knowledge


def search_knowledge_base(query: str, k: int = 3) -> str:
    """Search knowledge base using TF-IDF similarity."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    print(f"🔍 Looking for knowledge base at: {CHUNKS_DB_PATH}")
    print(f"📁 File exists: {os.path.exists(CHUNKS_DB_PATH)}")

    # Build if doesn't exist
    chunks = build_vector_store()

    if not chunks:
        print("⚠️ No chunks found!")
        return ""
    print(f"📚 Searching through {len(chunks)} chunks...")

    # Build TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words="english")
    all_texts = chunks + [query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Get similarity between query and all chunks
    query_vector = tfidf_matrix[-1]
    chunk_vectors = tfidf_matrix[:-1]
    similarities = cosine_similarity(query_vector, chunk_vectors)[0]

    # Get top k most similar chunks
    top_indices = np.argsort(similarities)[::-1][:k]
    top_chunks = [chunks[i] for i in top_indices if similarities[i] > 0]

    if not top_chunks:
        print("⚠️ No relevant chunks found for query!")
        return ""

    context = "\n\n".join(top_chunks)
    print(f"📄 Context found ({len(context)} chars)")
    return context
