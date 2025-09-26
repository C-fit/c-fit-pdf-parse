# c-fit-pdf-parse
> PDF to Markdown API Server

Docling과 FastAPI를 이용하여, PDF 파일을 Markdown Text로 변환합니다.

docling의 `cpu-only` 버전을 이용하여 낮은 메모리와 CPU 환경에서도 동작합니다.

## How to
1. 이 Repo를 `git clone` 합니다.
2. uv를 설치하고 아래 명령어를 터미널에 입력합니다.
    ```
    cd c-fit-pdf-parse
    uv venv
    uv pip install --system \
    -r pyproject.toml \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match
    ```
3. 작업 시
    ```
    source .venv/bin/activate
    ```
    로 가상환경 진입 후 작업합니다. Windows의 경우,
    ```
    source .venv\Scripts\activate
    ```
로 사용할 수 있습니다.

가상환경은 `deactivate` 명령어로 중지 가능합니다.