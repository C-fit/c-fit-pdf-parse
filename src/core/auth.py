from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends, Security
from fastapi.security import APIKeyHeader
from src.core.config import settings


# 환경 변수에서 API 키를 불러옵니다. 실제 운영에서는 환경 변수로 관리하는 것이 필수입니다.
API_KEY = settings.PARSE_API_KEY
API_KEY_NAME = "X-API-KEY" # 요청 헤더의 이름

api_key_header_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header_scheme)):
    """API 키를 검증하는 의존성 함수"""
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Invalid or missing API Key"
        )
