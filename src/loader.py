import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

SUPPORTED_EXTENSIONS = (".pdf", ".docx")
DEFAULT_CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))


def load_documents(folder_path: str | Path) -> list[Document]:
    """
    Load all supported documents (PDF, DOCX) from a directory.

    Args:
        folder_path (str | Path): Path to directory containing documents.

    Returns:
        list[Document]: List of loaded LangChain documents with sanitized metadata.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ValueError: If no supported files are found or no content could be extracted.
    """
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Invalid folder path: {folder}")

    files = [
        path
        for path in sorted(folder.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise ValueError("No supported files found. Please upload PDF or DOCX files.")

    documents: list[Document] = []

    for file_path in files:
        loaded = _load_single_document(file_path)
        documents.extend(loaded)

    # Filter out empty or whitespace-only pages
    documents = [doc for doc in documents if doc.page_content and doc.page_content.strip()]

    if not documents:
        raise ValueError("No content found in any documents.")

    return documents


def _load_single_document(file_path: Path) -> list[Document]:
    """
    Load a single document using the appropriate loader based on its extension.

    Args:
        file_path (Path): Path to the target document.

    Returns:
        list[Document]: Loaded document chunks/pages with normalized metadata.
    """
    extension = file_path.suffix.lower()

    try:
        if extension == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
        elif extension == ".docx":
            loader = Docx2txtLoader(str(file_path))
            docs = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            f"Could not read '{file_path.name}'. The file may be invalid or corrupted."
        ) from exc

    for doc in docs:
        doc.metadata = doc.metadata or {}
        doc.metadata["source"] = file_path.name
        doc.metadata["file_name"] = file_path.name

        if "page" in doc.metadata and doc.metadata["page"] is not None:
            try:
                doc.metadata["page"] = int(doc.metadata["page"]) + 1
            except (ValueError, TypeError):
                doc.metadata["page"] = None
        else:
            doc.metadata["page"] = None

    return docs


def split_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Document]:
    """
    Split loaded documents into chunks for embedding and vector search.

    Args:
        documents (list[Document]): List of documents to split.
        chunk_size (int | None, optional): Size of text chunks. Defaults to CHUNK_SIZE from env or 1000.
        chunk_overlap (int | None, optional): Overlap between text chunks. Defaults to CHUNK_OVERLAP from env or 150.

    Returns:
        list[Document]: Split document chunks.

    Raises:
        ValueError: If documents list is empty.
    """
    if not documents:
        raise ValueError("No documents provided for splitting")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or DEFAULT_CHUNK_SIZE,
        chunk_overlap=chunk_overlap or DEFAULT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents(documents)


def count_source_files(folder_path: str | Path) -> int:
    """
    Count the number of supported documents (PDF, DOCX) in a folder.

    Args:
        folder_path (str | Path): Path to the folder.

    Returns:
        int: Number of supported files found.
    """
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return 0

    return sum(
        1
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


# Alias to maintain backward compatibility
count_source_fils = count_source_files