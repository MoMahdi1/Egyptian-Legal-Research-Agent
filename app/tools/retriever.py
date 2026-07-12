from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ======================================================
# Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CHROMA_PATH = BASE_DIR / "data" / "chroma_db"

# ======================================================
# Configuration
# ======================================================

EMBEDDING_MODEL = "intfloat/multilingual-e5-small"

DEFAULT_TOP_K = 10

# ======================================================
# Embedding Model
# ======================================================

# Loaded once when the application starts
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# ======================================================
# Vector Store
# ======================================================

# Loaded once when the application starts
vectorstore = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings,
)

# ======================================================
# Retriever
# ======================================================

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": DEFAULT_TOP_K
    }
)


def get_vectorstore():
    """Return the initialized Chroma vector store."""
    return vectorstore


def get_retriever():
    """Return the initialized retriever."""
    return retriever