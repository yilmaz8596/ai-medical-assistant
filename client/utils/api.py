import requests 
from config import API_URL


def upload_pdf_api(files): 
    files_payload = [("files", (file.name, file.read(), "application/pdf")) for file in files]
    return requests.post(f"{API_URL}/upload_pdf/", files=files_payload)


def ask_question_api(question): 
    return requests.post(f"{API_URL}/ask/", data={"question": question})