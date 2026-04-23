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

## 디렉토리 구조 (예정)

```
receipt-tracker/
├── frontend/
│   ├── src/
│   │   ├── pages/          # HomePage, DetailPage
│   │   └── components/     # UploadArea, ExpenseList, SummaryCard 등
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── routers/            # upload.py, expenses.py, summary.py
│   ├── services/           # ocr_service.py (Upstage), storage_service.py
│   ├── data/expenses.json
│   └── requirements.txt
└── vercel.json
```

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
npm run dev        # 개발 서버 :5173
npm run build      # 프로덕션 빌드
```

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/upload` | 영수증 이미지/PDF 업로드 → OCR 파싱 → 지출 데이터 반환 |
| GET | `/api/expenses` | 지출 목록 조회 (선택: `start_date`/`end_date` 쿼리 파라미터) |
| DELETE | `/api/expenses/{id}` | 지출 항목 삭제 |
| PUT | `/api/expenses/{id}` | 지출 항목 수정 |
| GET | `/api/summary` | 카테고리/기간별 지출 통계 |

## 지출 데이터 스키마

```json
{
  "id": "uuid",
  "created_at": "ISO8601",
  "store_name": "string",
  "receipt_date": "YYYY-MM-DD",
  "receipt_time": "HH:MM",
  "category": "식비|카페|쇼핑|교통|의료|문화|기타",
  "items": [{"name": "string", "quantity": 1, "price": 0}],
  "subtotal": 0,
  "discount": 0,
  "tax": 0,
  "total_amount": 0,
  "payment_method": "string",
  "raw_image_path": "string"
}
```

## 주요 제약 사항

- **Vercel serverless**: 요청 간 `expenses.json`이 유지되지 않음. Vercel KV/Blob 스토리지 사용 또는 프론트엔드 localStorage 폴백 처리 필요.
- **PDF 지원**: `pdf2image`는 Poppler 바이너리 필요 — Vercel 호환성 확인 필수. 클라이언트 사이드에서 PDF→이미지 변환 방식도 고려.
- **파일 업로드 제한**: 영수증 1건당 최대 10MB (JPG, PNG, PDF).

## 구현 단계 (PRD 기준)

1. ✅ 프로젝트 셋업 — GitHub, `.env`, venv, `requirements.txt`, React+Vite 스캐폴딩
2. 백엔드 OCR 연동 — FastAPI + Upstage Vision LLM (LangChain)
3. 백엔드 CRUD API — 지출 라우터 + JSON 스토리지 서비스
4. 프론트엔드 스캐폴딩 — Vite + TailwindCSS + Axios 기본 설정
5. 업로드 컴포넌트 — 드래그앤드롭, 미리보기, OCR 호출
6. 지출 목록 + 상세 컴포넌트
7. 요약 대시보드 + 날짜 필터링
8. Vercel 배포 + `/images/` 샘플 영수증으로 E2E 검증

## 참고 문서

- `PRD_영수증_지출관리앱.md` — 전체 요구사항, UI 디자인 시스템 (색상, 타이포그래피, 간격, 애니메이션), 구현 상세
- `프로그램개요서_영수증_지출관리앱.md` — 아키텍처 개요 및 1일 개발 일정
- `images/` — OCR 테스트용 샘플 영수증 이미지 11장 + PDF 1장

### 답변은 반드시 한국어로 해야합니다
