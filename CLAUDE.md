# CLAUDE.md

이 파일은 Claude Code(claude.ai/code)가 이 저장소에서 작업할 때 참고하는 가이드입니다.

## 프로젝트 개요

AI 기반 영수증 지출 관리 앱 — 1일 스프린트 MVP. 사용자가 영수증 이미지/PDF를 업로드하면 Upstage Vision LLM(LangChain 경유)으로 파싱하여 구조화된 지출 데이터를 JSON으로 저장한다.

## 기술 스택

- **Frontend**: React 18 + Vite 5 + TailwindCSS 3 + Axios
- **Backend**: Python FastAPI 0.111 + LangChain-Upstage 0.7.7 + Upstage Vision LLM (`document-digitization-vision`)
- **저장소**: JSON 파일 (`backend/data/expenses.json`) — DB 없음
- **배포**: Vercel (백엔드는 serverless functions, 프론트엔드는 static)
- **API 키**: `UPSTAGE_API_KEY`는 `.env`에 이미 설정되어 있음

## 실행 명령어

**Backend (프로젝트 루트에서 실행):**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/upload` | 영수증 이미지/PDF 업로드 → OCR 파싱 → 지출 데이터 반환 |
| GET | `/api/expenses` | 지출 목록 조회 |
| DELETE | `/api/expenses/{id}` | 지출 항목 삭제 |
| PUT | `/api/expenses/{id}` | 지출 항목 수정 |
| GET | `/api/summary` | 카테고리/기간별 지출 통계 |

## 구현 단계

1. ✅ 프로젝트 셋업
2. 백엔드 OCR 연동 — FastAPI + Upstage Vision LLM
3. 백엔드 CRUD API
4. 프론트엔드 스캐폴딩
5. 업로드 컴포넌트
6. 지출 목록 + 상세 컴포넌트
7. 요약 대시보드 + 날짜 필터링
8. Vercel 배포 + E2E 검증

### 답변은 반드시 한국어로 해야합니다
