
from fastapi import APIRouter, File, UploadFile
from typing import List 
from ..modules.load_vector_store import load_vector_store
from fastapi.responses import JSONResponse
from ..logger import logger

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received {len(files)} files for upload.")
        load_vector_store(files)
        logger.info("Files processed and vector store updated successfully.")
        return JSONResponse(status_code=200, content={"message": "Files uploaded and processed successfully."})
    except Exception as e:
        logger.error(f"Error processing uploaded files: {str(e)}")
        return JSONResponse(status_code=500, content={"message": f"An error occurred while processing the files: {str(e)}"})
