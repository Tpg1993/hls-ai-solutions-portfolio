from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hcp import HCP
from app.models.prescription import Prescription
from app.models.interaction import Interaction

async def fetch_hcp_dossier(db: AsyncSession, hcp_id: str) -> Dict[str, Any]:
    stmt = select(HCP).where(HCP.id == hcp_id)
    res = await db.execute(stmt)
    hcp = res.scalar_one_or_none()
    if not hcp:
        return {}
    return {
        "id": hcp.id,
        "npi": hcp.npi_synthetic,
        "name": f"Dr. {hcp.first_name} {hcp.last_name}",
        "specialty": hcp.specialty,
        "hospital": hcp.hospital_affiliation,
        "city": hcp.city,
        "state": hcp.state,
        "decile": hcp.decile,
        "digital_affinity": hcp.digital_affinity,
        "territory_id": hcp.territory_id,
    }

async def fetch_hcp_prescriptions(db: AsyncSession, hcp_id: str) -> List[Dict[str, Any]]:
    stmt = select(Prescription).where(Prescription.hcp_id == hcp_id).order_by(Prescription.month_year.desc()).limit(12)
    res = await db.execute(stmt)
    rows = res.scalars().all()
    return [
        {
            "month_year": r.month_year,
            "trx_count": r.trx_count,
            "nrx_count": r.nrx_count,
            "competitor_trx_count": r.competitor_trx_count,
        }
        for r in reversed(rows)
    ]

async def fetch_hcp_interactions(db: AsyncSession, hcp_id: str) -> List[Dict[str, Any]]:
    stmt = select(Interaction).where(Interaction.hcp_id == hcp_id).order_by(Interaction.interaction_date.desc()).limit(5)
    res = await db.execute(stmt)
    rows = res.scalars().all()
    return [
        {
            "id": r.id,
            "date": str(r.interaction_date),
            "channel": r.channel,
            "rep_name": r.rep_name,
            "topics": r.topics_discussed,
            "sentiment": r.sentiment,
            "notes": r.notes,
        }
        for r in rows
    ]
