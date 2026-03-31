import streamlit as st 
from utils.api import upload_pdf_api 


def render_uploader():
    st.sidebar.header("Upload Medical Documents (PDF)")
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if st.sidebar.button("Upload DB") and uploaded_files:
        with st.spinner("Uploading and processing files..."):
            response = upload_pdf_api(uploaded_files)
            if response.status_code == 200:
                st.success("Files uploaded and processed successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")