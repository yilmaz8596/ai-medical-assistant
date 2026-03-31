import os
import time
from pathlib import Path

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from tqdm.auto import tqdm

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load environment from current working directory first, then fallback
load_dotenv()
env_path = Path(__file__).resolve().parents[1] / ".env"
if not os.getenv("GOOGLE_API_KEY") and env_path.exists():
    load_dotenv(dotenv_path=env_path)

PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-index")
UPLOAD_DIR = "./uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def _ensure_required_env() -> tuple[str, str]:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing.")
    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY is missing.")

    os.environ["GOOGLE_API_KEY"] = google_api_key
    return google_api_key, pinecone_api_key


def _get_index(pc: Pinecone):
    existing_indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,
            metric="dotproduct",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV),
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            print("Waiting for Pinecone index to be ready...")
            time.sleep(5)

    return pc.Index(PINECONE_INDEX_NAME)


def load_vector_store(uploaded_files):
    _, pinecone_api_key = _ensure_required_env()
    pc = Pinecone(api_key=pinecone_api_key)
    index = _get_index(pc)
    embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", output_dimensionality=768)
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadata = []
        for chunk in chunks:
            chunk_metadata = dict(chunk.metadata or {})
            chunk_metadata["text"] = chunk.page_content
            metadata.append(chunk_metadata)

        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"Embedding chunks for {file_path}...")
        embedding = embed_model.embed_documents(texts)

        print(f"Upserting chunks to Pinecone for {file_path}...")
        with tqdm(total=len(embedding), desc=f"Upserting {file_path}") as progress:
            index.upsert(vectors=list(zip(ids, embedding, metadata)))
            progress.update(len(embedding))

        print(f"Finished processing {file_path}.")