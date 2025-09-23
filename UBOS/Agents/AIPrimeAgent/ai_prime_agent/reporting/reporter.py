"""
UBOS Blueprint: Reporting Utility

Philosophy: High-Leverage Actions + Systems Over Willpower
Strategic Purpose: Turn orchestration results into reusable artifacts (JSON, MD,
and optional Mermaid) for sharing and follow-up without manual work.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def _md_escape(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;")


def _to_html(result: Dict[str, Any]) -> str:
    research = result.get("research", {})
    consult = result.get("consultation", {})
    recs = consult.get("recommendations", []) or []
    notes = consult.get("alignment_notes", []) or []
    citations = research.get("citations", []) or []

    def esc(s: str) -> str:
        return (_md_escape(s)).replace("\n", "<br>")

    html = [
        "<html><head><meta charset='utf-8'><title>UBOS Prime Report</title>",
        "<style>body{font-family:system-ui, sans-serif;max-width:820px;margin:24px auto;line-height:1.5} code,pre{font-family:ui-monospace, SFMono-Regular, Menlo, monospace} .meta{color:#555}</style>",
        "</head><body>",
    ]
    html.append(f"<h1>UBOS Prime Report</h1>")
    html.append("<div class='meta'>")
    html.append(f"<div><b>Correlation</b>: {result.get('correlation_id','')}</div>")
    html.append(f"<div><b>Blueprint Mission</b>: {esc(str(result.get('blueprint_mission','')))}</div>")
    html.append(f"<div><b>Final Confidence</b>: {result.get('final_confidence',0):.2f}</div>")
    html.append("</div>")

    html.append("<h2>Research Summary</h2>")
    html.append(f"<p>{esc(research.get('content','(no content)'))}</p>")
    if citations:
        html.append("<h3>Citations</h3><ul>")
        for c in citations:
            html.append(f"<li><a href='{c}'>{esc(c)}</a></li>")
        html.append("</ul>")

    html.append("<h2>UBOS Recommendations</h2><ul>")
    for r in recs:
        title = esc(r.get("title", "(untitled)"))
        rationale = esc(r.get("rationale", ""))
        conf = r.get("confidence", 0)
        html.append(f"<li><b>{title}</b> <span class='meta'>(confidence {conf:.2f})</span><br>{rationale}</li>")
    html.append("</ul>")
    if notes:
        html.append("<h3>Alignment Notes</h3><ul>")
        for n in notes:
            html.append(f"<li>{esc(n)}</li>")
        html.append("</ul>")

    pause = result.get("pause", {})
    validation = result.get("validation", {})
    html.append("<h2>Pause and Validation</h2>")
    html.append(f"<div>Pre-Pause: {pause.get('pre',{}).get('status','n/a')}</div>")
    html.append(f"<div>Post-Pause: {pause.get('post',{}).get('status','n/a')}</div>")
    html.append(f"<div>Validation: {validation.get('status','n/a')}</div>")

    html.append("</body></html>")
    return "".join(html)


def write_report(result: Dict[str, Any], out_dir: Path | str) -> Dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base = out / f"prime_report_{ts}"

    # Write JSON result
    json_path = base.with_suffix(".json")
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    # Write Markdown summary
    research = result.get("research", {})
    consult = result.get("consultation", {})
    recs = consult.get("recommendations", []) or []
    notes = consult.get("alignment_notes", []) or []
    citations = research.get("citations", []) or []
    md_lines = []
    md_lines.append(f"# UBOS Prime Report — {ts}")
    md_lines.append("")
    md_lines.append(f"- Correlation: `{result.get('correlation_id', '')}`")
    md_lines.append(f"- Blueprint Mission: {_md_escape(str(result.get('blueprint_mission', '')))}")
    md_lines.append(f"- Final Confidence: {result.get('final_confidence', 0):.2f}")
    md_lines.append("")
    md_lines.append("## Research Summary")
    md_lines.append(_md_escape(research.get("content", "(no content)")))
    if citations:
        md_lines.append("")
        md_lines.append("### Citations")
        for c in citations:
            md_lines.append(f"- {c}")
    md_lines.append("")
    md_lines.append("## UBOS Recommendations")
    for r in recs:
        title = r.get("title", "(untitled)")
        rationale = r.get("rationale", "")
        confidence = r.get("confidence", 0)
        md_lines.append(f"- {title} (confidence {confidence:.2f})")
        if rationale:
            md_lines.append(f"  - {rationale}")
    if notes:
        md_lines.append("")
        md_lines.append("### Alignment Notes")
        for n in notes:
            md_lines.append(f"- {n}")
    md_lines.append("")
    md_lines.append("## Pause and Validation")
    pause = result.get("pause", {})
    validation = result.get("validation", {})
    md_lines.append(f"- Pre-Pause: {pause.get('pre', {}).get('status', 'n/a')}")
    md_lines.append(f"- Post-Pause: {pause.get('post', {}).get('status', 'n/a')}")
    md_lines.append(f"- Validation: {validation.get('status', 'n/a')}")

    md_path = base.with_suffix(".md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # Optional Mermaid
    mermaid = consult.get("mermaid") or consult.get("mermaid_diagram")
    mermaid_path = ""
    if isinstance(mermaid, str) and mermaid.strip():
        mermaid_path = str(base.with_suffix(".mmd"))
        Path(mermaid_path).write_text(mermaid, encoding="utf-8")

    # HTML
    html_path = base.with_suffix(".html")
    html_path.write_text(_to_html(result), encoding="utf-8")

    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "mermaid": mermaid_path,
        "html": str(html_path),
    }


__all__ = ["write_report"]
