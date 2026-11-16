
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent

# Separate index for local embeddings
VECTOR_DIR = BASE_DIR / "data" / "faiss_index_local"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={
        "normalize_embeddings": True,
        "batch_size": 32,
    },
)


def load_document(file_path: str) -> list[Document]:
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    documents = []

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": path.name,
                            "page": page_number,
                        },
                    )
                )

    elif path.suffix.lower() == ".txt":
        text = path.read_text(encoding="utf-8-sig")

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": path.name},
                )
            )

    else:
        raise ValueError("Only PDF and TXT files are supported.")

    if not documents:
        raise ValueError(
            f"No readable text found in document: {path.name}"
        )

    return documents


def create_vector_store(file_paths: list[str]) -> int:
    documents = []

    for file_path in file_paths:
        documents.extend(load_document(file_path))

    if not documents:
        raise ValueError("No documents were loaded.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks were created.")

    print(f"Loaded documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")
    print("Generating local embeddings...")

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    vector_store.save_local(str(VECTOR_DIR))

    print(f"FAISS database saved: {VECTOR_DIR}")

    return len(chunks)


def load_vector_store():
    index_path = VECTOR_DIR / "index.faiss"

    if not index_path.exists():
        raise FileNotFoundError(
            "No FAISS database found. Upload and process documents first."
        )

    return FAISS.load_local(
        str(VECTOR_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def search_documents(question: str, k: int = 4) -> str:
    if not question.strip():
        raise ValueError("Please enter a question.")

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k,
    )

    if not results:
        return "No relevant information was found in uploaded documents."

    context = []

    for document in results:
        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page")

        location = (
            f"{source}, page {page}"
            if page else source
        )

        context.append(
            f"Source: {location}\n{document.page_content}"
        )

    return "\n\n---\n\n".join(context)


@tool
def ask_documents(question: str) -> str:
    """Search uploaded PDF and TXT documents for relevant information.
    Use this tool when the user asks questions about uploaded documents.
    """
    try:
        return search_documents(question)

    except FileNotFoundError as error:
        return str(error)

    except Exception as error:
        return f"Document search failed: {error}"


RAG_TOOL = ask_documents
