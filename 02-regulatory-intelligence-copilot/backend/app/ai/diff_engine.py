import time
from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.guidance import GuidanceDocument, GuidanceSection
from app.models.diff import GuidanceVersionDiff
from app.ai.router import llm_router
from app.core.logging import logger

async def analyze_cross_version_diff(
    db: AsyncSession,
    baseline_doc_id: str,
    comparison_doc_id: str,
) -> Dict[str, Any]:
    """
    Compares baseline vs comparison guidance documents, analyzing structural and semantic shifts.
    """
    start_time = time.perf_counter()

    # Check existing precomputed diffs in DB
    stmt = select(GuidanceVersionDiff).where(
        GuidanceVersionDiff.baseline_doc_id == baseline_doc_id,
        GuidanceVersionDiff.comparison_doc_id == comparison_doc_id,
    )
    res = await db.execute(stmt)
    diff_records = res.scalars().all()

    # Get document titles
    doc_res = await db.execute(
        select(GuidanceDocument).where(GuidanceDocument.id.in_([baseline_doc_id, comparison_doc_id]))
    )
    docs = {d.id: d for d in doc_res.scalars().all()}
    base_doc = docs.get(baseline_doc_id)
    comp_doc = docs.get(comparison_doc_id)

    diff_items = []
    for d in diff_records:
        diff_items.append({
            "id": d.id,
            "section_number": d.section_number,
            "section_title": d.section_title,
            "change_type": d.change_type,
            "old_text": d.old_text,
            "new_text": d.new_text,
            "semantic_impact": d.semantic_impact,
            "impact_severity": d.impact_severity,
        })

    # Summary of changes
    critical_count = sum(1 for d in diff_items if d["impact_severity"] == "CRITICAL")
    high_count = sum(1 for d in diff_items if d["impact_severity"] == "HIGH")

    return {
        "baseline_doc": {
            "id": base_doc.id if base_doc else baseline_doc_id,
            "title": base_doc.title if base_doc else "Baseline Version",
            "authority": base_doc.authority if base_doc else "",
            "version": base_doc.version if base_doc else "1.0",
        },
        "comparison_doc": {
            "id": comp_doc.id if comp_doc else comparison_doc_id,
            "title": comp_doc.title if comp_doc else "Comparison Version",
            "authority": comp_doc.authority if comp_doc else "",
            "version": comp_doc.version if comp_doc else "2.0",
        },
        "total_changes": len(diff_items),
        "critical_changes": critical_count,
        "high_priority_changes": high_count,
        "changes": diff_items,
        "analysis_latency_ms": round((time.perf_counter() - start_time) * 1000, 2),
    }
