"""Build the public knowledge base from corpus/manifest.yaml.

For each source: fetch the repo at its pinned commit, select the files the
manifest lists, strip site-generator markup, and write clean markdown with
provenance front matter (source, URL, license) to corpus/public/<source id>/.

Run from the repo root:
    python scripts/build_corpus.py            # fetch and build everything
    python scripts/build_corpus.py --clean    # delete corpus/public first
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "corpus" / "manifest.yaml"
OUT = ROOT / "corpus" / "public"
CACHE = ROOT / ".cache" / "sources"


def fetch(repo: str, commit: str) -> Path:
    """Shallow-fetch one commit of a repo into the cache and return its path."""
    name = repo.rstrip("/").split("github.com/")[-1].replace("/", "__")
    dest = CACHE / f"{name}@{commit[:12]}"
    if (dest / ".git").exists():
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    run = lambda *args: subprocess.run(["git", *args], cwd=dest, check=True,
                                       capture_output=True, text=True)
    run("init", "-q")
    run("remote", "add", "origin", repo)
    run("fetch", "-q", "--depth", "1", "origin", commit)
    run("checkout", "-q", "FETCH_HEAD")
    return dest


def select(repo_dir: Path, include: list[str], exclude: list[str]) -> list[Path]:
    files: set[Path] = set()
    for pattern in include:
        files.update(p for p in repo_dir.glob(pattern) if p.is_file())
    rel = lambda p: p.relative_to(repo_dir).as_posix()
    return sorted(p for p in files if not any(fnmatch.fnmatch(rel(p), x) for x in exclude))


FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def split_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[m.end():]


def clean_markdown(body: str) -> str:
    """Remove site-generator markup while keeping headings, lists, and tables."""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)                # HTML comments
    body = re.sub(r"\{%-?.*?-?%\}", "", body, flags=re.S)             # Liquid/Nunjucks tags
    body = re.sub(r"\{\{.*?\}\}", "", body, flags=re.S)               # template expressions
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)                  # images
    body = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])+)\]\([^)]*\)", r"\1", body)  # links -> link text
    body = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", body)             # reference links
    body = re.sub(r"^\[[^\]]+\]:\s*\S+.*$", "", body, flags=re.M)     # link definitions
    body = re.sub(r"</?(div|span|section|aside|figure|figcaption|img|br|p|a|button|svg|path|use|iframe)\b[^>]*>",
                  "", body, flags=re.I)
    body = re.sub(r"\{:[^}]*\}", "", body)                            # kramdown attributes
    body = re.sub(r"\{#[^}]*\}", "", body)                            # heading anchor ids
    body = re.sub(r"\{\.[^}]*\}", "", body)                           # CSS class attributes
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip() + "\n"


def intro_from_front_matter(meta: dict, body: str) -> str:
    """Some pages keep their opening content in front matter (18F method cards); restore it."""
    method = meta.get("method") if isinstance(meta.get("method"), dict) else {}
    parts = []
    for key, label in (("what", "What it is"), ("why", "Why use it"), ("timeRequired", "Time required")):
        if method.get(key):
            parts.append(f"**{label}:** {method[key]}")
    if not parts and meta.get("description"):
        desc = str(meta["description"]).strip()
        if desc[:40] not in body:
            parts.append(desc)
    return "\n\n".join(parts + [body]) if parts else body


def title_for(meta: dict, body: str, path: Path) -> str:
    title = meta.get("title")
    if meta.get("play_number"):
        title = f"Play {meta['play_number']}: {title}"
    if not title:
        m = re.search(r"^#\s+(.+)$", body, flags=re.M)
        title = m.group(1).strip() if m else path.stem.replace("-", " ").capitalize()
    return str(title).strip()


def url_for(src: dict, meta: dict, rel: str) -> str:
    if src.get("url_from_permalink") and meta.get("permalink"):
        return src["url_base"].rstrip("/") + "/" + str(meta["permalink"]).lstrip("/")
    if src["id"] == "usds-playbook" and meta.get("play_number"):
        return f"{src['url_base'].rstrip('/')}/#play{meta['play_number']}"
    return src["url_base"] + rel


def build(clean: bool) -> int:
    manifest = yaml.safe_load(MANIFEST.read_text())
    if clean and OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for src in manifest["sources"]:
        repo_dir = fetch(src["repo"], src["commit"])
        files = select(repo_dir, src.get("include", []), src.get("exclude", []))
        dest = OUT / src["id"]
        dest.mkdir(parents=True, exist_ok=True)
        for path in files:
            rel = path.relative_to(repo_dir).as_posix()
            meta, body = split_front_matter(path.read_text(encoding="utf-8"))
            body = clean_markdown(intro_from_front_matter(meta, body))
            if len(body.split()) < 40:          # navigation stubs and empty index pages
                continue
            header = {
                "title": title_for(meta, body, path),
                "source_id": src["id"],
                "source_title": src["title"],
                "author": src["author"],
                "license": src["license"],
                "source_url": url_for(src, meta, rel),
                "source_path": rel,
                "source_commit": src["commit"],
            }
            out_name = re.sub(r"^content/", "", rel).replace("/", "__")
            (dest / out_name).write_text(
                "---\n" + yaml.safe_dump(header, sort_keys=False, allow_unicode=True) + "---\n\n" + body,
                encoding="utf-8")
            total += 1
        print(f"{src['id']:28s} {len(list(dest.glob('*.md'))):3d} documents")
    print(f"{'total':28s} {total:3d} documents -> {OUT.relative_to(ROOT)}")
    write_sources(manifest)
    return 0


def write_sources(manifest: dict) -> None:
    """SOURCES.md: what is in the public knowledge base and under which license."""
    lines = [
        "# Sources",
        "",
        "Everything in `corpus/public/` comes from the sources below, fetched at the pinned commit by "
        "`scripts/build_corpus.py`. Each document keeps its source URL and license in its front matter, and "
        "every answer cites the passage it used. Nothing licensed or proprietary is in this repository; "
        "private material goes in `corpus/private/`, which git ignores.",
        "",
        "| Source | Author | License | Documents | Words | Repository (commit) |",
        "|---|---|---|---|---|---|",
    ]
    for src in manifest["sources"]:
        files = sorted((OUT / src["id"]).glob("*.md"))
        words = sum(len(split_front_matter(f.read_text())[1].split()) for f in files)
        repo = src["repo"].replace("https://github.com/", "")
        lines.append(f"| {src['title']} | {src['author']} | {src['license']} | {len(files)} | {words:,} | "
                     f"[{repo}]({src['repo']}/tree/{src['commit']}) (`{src['commit'][:7]}`) |")
    lines += [
        "",
        "The 18F guides and the Digital Services Playbook are works of the U.S. government, in the public "
        "domain in the United States and dedicated worldwide under CC0 1.0. Their inclusion does not imply "
        "endorsement by GSA, 18F, or the U.S. Digital Service. The author's own documents are MIT licensed.",
        "",
        "ADKAR® and Prosci® are registered trademarks of Prosci Inc. This project is not affiliated with or "
        "endorsed by Prosci and contains no Prosci course materials, assessments, or templates.",
    ]
    (ROOT / "SOURCES.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--clean", action="store_true", help="delete corpus/public before building")
    sys.exit(build(ap.parse_args().clean))
