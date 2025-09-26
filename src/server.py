import os
import shutil
import tempfile
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from src.pdf_loader import load_pdf

# from dotenv import load_dotenv
# load_dotenv()

app = FastAPI()

# --- 설정 (Configuration) ---

PRODUCTION_ORIGINS = [
    "https://your-production-frontend.com",
]

origins = [
    "http:localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # NOTE: 배포 시 PRODUCTION_ORIGINS로 설정
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

ALLOWED_EXTENSIONS = {"pdf"}
ALLOWED_MIME_TYPES = {"application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def is_safe_file(filename: str, content_type: str) -> bool:
    """파일 확장자와 MIME 타입을 검사하여 안전한 파일인지 확인합니다."""
    if '.' not in filename:
        return False
    
    # 파일 확장자 검사
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
        
    # MIME 타입 검사
    if content_type not in ALLOWED_MIME_TYPES:
        return False
        
    return True


@app.post("/preprocess-resume")
async def preprocess_resume_endpoint(resume_file: UploadFile = File(...)):
    """PDF 파일을 파싱하여 Markdown 문자열로 변환합니다."""
    
    # 파일 크기 검증
    if resume_file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, detail=f"File size exceeds the limit of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
        
    # 파일 타입 및 확장자 검증
    if not is_safe_file(resume_file.filename, resume_file.content_type):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are allowed."
        )

    temp_file_path = None
    try:
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}.pdf")

        with open(temp_file_path, "wb") as tmp_file:
            shutil.copyfileobj(resume_file.file, tmp_file)

        # 6. 블로킹 작업(동기 함수)을 별도 스레드에서 실행
        # CPU를 많이 사용하는 load_pdf 함수가 서버의 메인 이벤트 루프를 막지 않도록 합니다.
        result = await run_in_threadpool(load_pdf, temp_file_path)
        
        return {"resume": result}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the file.")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
