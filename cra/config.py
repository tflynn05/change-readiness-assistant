"""Settings, read from environment variables with sensible defaults."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    """Read KEY=VALUE lines from .env without overriding the real environment."""
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


def _extra_private_dirs() -> list[Path]:
    """Folders named in CRA_PRIVATE_DIR (separated by the OS path separator, ':' on macOS).

    Relative paths resolve against the project folder, so `../Certifications/Prosci` works
    wherever the project lives. Files are read in place; nothing is copied into the project.
    """
    raw = os.environ.get("CRA_PRIVATE_DIR", "").strip()
    dirs = []
    for part in raw.split(os.pathsep) if raw else []:
        part = part.strip()
        if part:
            path = Path(part).expanduser()
            dirs.append((path if path.is_absolute() else ROOT / path).resolve())
    return dirs


@dataclass
class Settings:
    public_dir: Path = ROOT / "corpus" / "public"
    private_dir: Path = ROOT / "corpus" / "private"
    extra_private_dirs: list = field(default_factory=_extra_private_dirs)
    index_dir: Path = ROOT / ".index"
    # Retrieval
    mode: str = os.environ.get("CRA_RETRIEVAL", "bm25")          # bm25 | embed | hybrid
    top_k: int = int(os.environ.get("CRA_TOP_K", "6"))
    # Each match is expanded to its surrounding section, up to this many words (0 = off).
    context_words: int = int(os.environ.get("CRA_CONTEXT_WORDS", "600"))
    embed_model: str = os.environ.get("CRA_EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    # Grounding gate: below these scores the assistant declines without calling the model.
    # Calibrated by `cra eval --retrieval-only`; see eval/results/retrieval.md.
    min_bm25: float = float(os.environ.get("CRA_MIN_BM25", "0.14"))
    min_cosine: float = float(os.environ.get("CRA_MIN_COSINE", "0.55"))
    # Generation
    # Current models think before answering, and thinking counts toward max_tokens, so the
    # limits leave room for it. Effort sets how much the model thinks (low|medium|high|xhigh|max).
    model: str = os.environ.get("CRA_MODEL", "claude-sonnet-5-5")
    effort: str = os.environ.get("CRA_EFFORT", "medium")
    max_tokens: int = int(os.environ.get("CRA_MAX_TOKENS", "8000"))
    judge_model: str = os.environ.get("CRA_JUDGE_MODEL", "claude-opus-5-5")
    judge_effort: str = os.environ.get("CRA_JUDGE_EFFORT", "medium")
    judge_max_tokens: int = int(os.environ.get("CRA_JUDGE_MAX_TOKENS", "16000"))
    # Guardrails
    min_citation_coverage: float = float(os.environ.get("CRA_MIN_CITATION_COVERAGE", "0.6"))
    max_private_quote_words: int = int(os.environ.get("CRA_MAX_PRIVATE_QUOTE_WORDS", "25"))
    include_private: bool = os.environ.get("CRA_INCLUDE_PRIVATE", "1") != "0"
    extra: dict = field(default_factory=dict)

    @property
    def private_dirs(self) -> list[Path]:
        return [self.private_dir, *self.extra_private_dirs] if self.include_private else []
