import os 
import shutill 
from fastapi import UploadFile 
import tempfile


UPLOAD_DIR = "./uploads"

def save_uploaded_file(files:list[UploadFile]) -> list[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    saved_paths=[]
    
    for file in files:
        save_path=os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            shutill.copyfileobj(file.file, f)
        saved_paths.append(save_path)
    return saved_paths

