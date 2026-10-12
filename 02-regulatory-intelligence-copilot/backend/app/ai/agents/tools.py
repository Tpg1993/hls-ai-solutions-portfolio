from typing import List, Dict, Any, Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.guidance import GuidanceDocument, GuidanceSection

async def hybrid_search_regulatory_sections(
    db: AsyncSession,
    query: str,
    authority: Optional[str] = None,
    therapeutic_area: Optional[str] = None,
    limit: int = 6,
) -> List[Dict[str, Any]]:
    """
    Executes hybrid keyword and metadata matching over guidance sections.
    """
    tokens = [t.strip().lower() for t in query.split() if len(t.strip()) > 3]

    stmt = select(GuidanceSection, GuidanceDocument).join(
        GuidanceDocument, GuidanceSection.document_id == GuidanceDocument.id
    )

    filters = []
    if authority:
        filters.append(GuidanceDocument.authority.ilike(f"%{authority}%"))
    if therapeutic_area:
        filters.append(GuidanceDocument.therapeutic_area.ilike(f"%{therapeutic_area}%"))

    # Keyword match conditions
    token_conditions = []
    for t in tokens[:4]:
        token_conditions.append(GuidanceSection.chunk_text.ilike(f"%{t}%"))
        token_conditions.append(GuidanceSection.keywords.ilike(f"%{t}%"))
        token_conditions.append(GuidanceSection.section_title.ilike(f"%{t}%"))

    if token_conditions:
        filters.append(or_(*token_conditions))

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.limit(limit)
    res = await db.execute(stmt)
    rows = res.all()

    results = []
    for sec, doc in rows:
        results.append({
            "section_id": sec.id,
            "document_id": doc.id,
            "authority": doc.authority,
            "document_title": doc.title,
            "therapeutic_area": doc.therapeutic_area,
            "section_number": sec.section_number,
            "section_title": sec.section_title,
            "page_number": sec.page_number,
            "chunk_text": sec.chunk_text,
            "keywords": sec.keywords,
        })

    # Fallback to broader match if strict filter returned 0 results
    if not results:
        fallback_stmt = select(GuidanceSection, GuidanceDocument).join(
            GuidanceDocument, GuidanceSection.document_id == GuidanceDocument.id
        ).limit(limit)
        fb_res = await db.execute(fallback_stmt)
        for sec, doc in fb_res.all():
            results.append({
                "section_id": sec.id,
                "document_id": doc.id,
                "authority": doc.authority,
                "document_title": doc.title,
                "therapeutic_area": doc.therapeutic_area,
                "section_number": sec.section_number,
                "section_title": sec.section_title,
                "page_number": sec.page_number,
                "chunk_text": sec.chunk_text,
                "keywords": sec.keywords,
            })

    return results
