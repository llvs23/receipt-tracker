#!/usr/bin/env python3
"""
코드 변경 시 PRD_영수증_지출관리앱.md 자동 갱신 훅 (PostToolUse)
- Write / Edit 툴 실행 후 자동 호출
- 변경 파일이 코드 파일이면 PRD 하단 '변경 이력' 섹션에 행 추가
- 파일 경로로 Phase를 추론하여 함께 기록
"""
import json
import sys
from datetime import datetime
from pathlib import Path

# ── 경로 설정 ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # .claude/hooks/ → 프로젝트 루트
PRD_PATH = PROJECT_ROOT / "PRD_영수증_지출관리앱.md"

# ── PRD 갱신 대상 제외 패턴 ───────────────────────────────────────────────────
SKIP_PATTERNS = [
    "PRD_영수증_지출관리앱.md",
    "프로그램개요서",
    "CLAUDE.md",
    "memory/",
    "venv/",
    "__pycache__",
    "node_modules/",
    ".gitignore",
    ".env",
    "settings",
    "hooks/",
]

# ── 파일 경로 패턴 → Phase 레이블 ─────────────────────────────────────────────
PHASE_MAP = [
    ("backend/main.py",                     "Phase 2 — FastAPI 앱 뼈대"),
    ("backend/services/storage_service",    "Phase 2 — 스토리지 서비스"),
    ("backend/services/ocr_service",        "Phase 2 — OCR 서비스"),
    ("backend/routers/upload",              "Phase 2 — 업로드 라우터"),
    ("backend/routers/expenses",            "Phase 3 — 지출 CRUD 라우터"),
    ("backend/routers/summary",             "Phase 3 — 통계 라우터"),
    ("frontend/vite.config",                "Phase 4 — Vite 설정"),
    ("frontend/tailwind.config",            "Phase 4 — TailwindCSS 설정"),
    ("frontend/src/api/",                   "Phase 4 — Axios 인스턴스"),
    ("frontend/src/components/Header",      "Phase 5 — Header 컴포넌트"),
    ("frontend/src/components/Toast",       "Phase 5 — Toast 컴포넌트"),
    ("frontend/src/components/Badge",       "Phase 5 — Badge 컴포넌트"),
    ("frontend/src/components/DropZone",    "Phase 5 — DropZone 컴포넌트"),
    ("frontend/src/components/ParsePreview","Phase 5 — ParsePreview 컴포넌트"),
    ("frontend/src/pages/UploadPage",       "Phase 5 — 업로드 페이지"),
    ("frontend/src/components/SummaryCard", "Phase 6 — SummaryCard 컴포넌트"),
    ("frontend/src/components/FilterBar",   "Phase 6 — FilterBar 컴포넌트"),
    ("frontend/src/components/ExpenseCard", "Phase 6 — ExpenseCard 컴포넌트"),
    ("frontend/src/pages/Dashboard",        "Phase 6 — 대시보드 페이지"),
    ("frontend/src/components/Modal",       "Phase 7 — Modal 컴포넌트"),
    ("frontend/src/components/ReceiptImage","Phase 7 — ReceiptImage 컴포넌트"),
    ("frontend/src/components/EditForm",    "Phase 7 — EditForm 컴포넌트"),
    ("frontend/src/pages/ExpenseDetail",    "Phase 7 — 상세 페이지"),
    ("vercel.json",                         "Phase 8 — Vercel 배포 설정"),
    ("frontend/package.json",               "Phase 4 — 프론트 패키지"),
    ("backend/requirements.txt",            "Phase 1 — 의존성"),
]


def should_skip(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    if normalized.endswith(".md"):
        return True
    return any(p in normalized for p in SKIP_PATTERNS)


def get_phase_label(file_path: str) -> str:
    normalized = file_path.replace("\\", "/").lower()
    for pattern, label in PHASE_MAP:
        if pattern.lower() in normalized:
            return label
    return ""


def append_change_log(file_path: str, tool_name: str):
    if not PRD_PATH.exists():
        return

    content = PRD_PATH.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        rel_path = Path(file_path).resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        rel_path = Path(file_path).name

    phase_label = get_phase_label(file_path)
    phase_str = f" — {phase_label}" if phase_label else ""
    new_row = f"| {timestamp} | `{rel_path}` | {tool_name}{phase_str} |\n"

    SECTION_HEADER = "## 17. 변경 이력\n"
    TABLE_HEADER = "| 시각 | 파일 | 작업 |\n|------|------|------|\n"

    if SECTION_HEADER not in content:
        content = content.rstrip() + (
            f"\n\n---\n\n{SECTION_HEADER}\n{TABLE_HEADER}{new_row}"
        )
    else:
        # 최신 항목이 위에 오도록 테이블 헤더 바로 다음에 삽입
        content = content.replace(TABLE_HEADER, TABLE_HEADER + new_row, 1)

    PRD_PATH.write_text(content, encoding="utf-8")


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    if data.get("tool_name") not in ("Write", "Edit"):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path or should_skip(file_path):
        sys.exit(0)

    append_change_log(file_path, data["tool_name"])
    sys.exit(0)


if __name__ == "__main__":
    main()
