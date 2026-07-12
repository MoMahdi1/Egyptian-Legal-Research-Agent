import os
import shutil
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = BASE_DIR / "data"
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"


# ==========================
# Load PDFs
# ==========================

def load_documents(path: Path):

    documents = []

    pdf_files = sorted(path.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found inside: {path}"
        )

    print(f"\nFound {len(pdf_files)} PDF files\n")

    for pdf in pdf_files:

        print(f"Loading -> {pdf.name}")

        loader = PyMuPDFLoader(str(pdf))

        docs = loader.load()

        for d in docs:
            d.metadata["file_name"] = pdf.name

        documents.extend(docs)

    print(f"\nLoaded {len(documents)} pages.\n")

    return documents


# ==========================
# Split Documents
# ==========================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50,

        separators=[
            "\nمادة",
            "مادة",
            "\n\n",
            "\n",
            ".",
            " "
        ]
    )

    chunks = splitter.split_documents(documents)
    
    print("\n========== SAMPLE CHUNKS ==========\n")

    for i, chunk in enumerate(chunks[:5], 1):
      print(f"\n----- Chunk {i} -----\n")
      print(chunk.page_content)

    for chunk in chunks:

        chunk.metadata["source"] = chunk.metadata.get(
            "source",
            ""
        )

        chunk.metadata["page"] = chunk.metadata.get(
            "page",
            ""
        )

        chunk.metadata["file_name"] = chunk.metadata.get(
            "file_name",
            ""
        )

    print(f"Created {len(chunks)} chunks.\n")

    return chunks


# ==========================
# Build Vector Store
# ==========================

def build_vectorstore(chunks):

    print("Loading Embedding Model...\n")

    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small"
    )

    print("Creating Chroma Database...\n")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    print("\nVector Database Created Successfully.")

    print(f"Saved to:\n{CHROMA_PATH}")

    return vectorstore


# ==========================
# Main
# ==========================

def run():

    DOCUMENTS_PATH.mkdir(exist_ok=True)

    if CHROMA_PATH.exists():

        print("Removing old Chroma Database...")

        shutil.rmtree(CHROMA_PATH)

    CHROMA_PATH.mkdir(exist_ok=True)

    documents = load_documents(DOCUMENTS_PATH)

    chunks = split_documents(documents)

    build_vectorstore(chunks)

    print("\nDone.")


if __name__ == "__main__":
    run()