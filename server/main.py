from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exceptions
from routes.upload_pdf import router as upload_pdf_router
from routes.ask_question import router as ask_question_router

app = FastAPI(title="Medical Assistant API", description="API for Medical Assistant Application", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware exception handlers 
app.middleware("http")(catch_exceptions)

app.include_router(upload_pdf_router, prefix="/api")
app.include_router(ask_question_router, prefix="/api")
