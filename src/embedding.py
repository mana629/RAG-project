import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

DEFAULT_EMBEDDING_MODEL = "models/text-embedding-004"


def get_embedding_model(model_name: str | None = None) -> GoogleGenerativeAIEmbeddings:
    """
    Initialize and return a Google Generative AI embedding model.

    Args:
        model_name (str, optional): Name of the embedding model to use.
            Defaults to the value of EMBEDDING_MODEL env var or 'models/text-embedding-004'.

    Returns:
        GoogleGenerativeAIEmbeddings: Initialized embedding model.

    Raises:
        ValueError: If GOOGLE_API_KEY is not set.
        RuntimeError: If the embedding model fails to initialize.

    Example:
        model = get_embedding_model()
        embeddings = model.embed_query("some text")
    """
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    model = model_name or os.getenv("EMBEDDING_MODEL", "").strip() or DEFAULT_EMBEDDING_MODEL

    try:
        embedding_model = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=api_key,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize embedding model: {str(exc)}") from exc

    return embedding_model


def get_embedding_model_name() -> str:
    """Return the configured embedding model name for UI display.

    Returns:
        str: Google Generative AI embedding model name currently configured.

    Example:
        print(get_embedding_model_name())
    """
    model_name = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    return model_name