from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.hcp import HCP
from app.models.prescription import Prescription
from app.models.interaction import Interaction
from app.models.recommendation import Recommendation
from app.schemas.hcp import HCPListItem, HCPDetailResponse, PrescriptionPoint, InteractionItem

class HCPService:
    @staticmethod
    async def get_hcps(
        db: AsyncSession,
        specialty: Optional[str] = None,
        territory_id: Optional[str] = None,
        decile_min: Optional[int] = None,
        priority_tier: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[HCPListItem], int]:
        query = select(HCP).outerjoin(Recommendation, HCP.id == Recommendation.hcp_id)

        if specialty:
            query = query.where(HCP.specialty == specialty)
        if territory_id:
            query = query.where(HCP.territory_id == territory_id)
        if decile_min is not None:
            query = query.where(HCP.decile >= decile_min)
        if priority_tier:
            query = query.where(Recommendation.priority_tier == priority_tier)
        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    HCP.first_name.ilike(search_term),
                    HCP.last_name.ilike(search_term),
                    HCP.npi_synthetic.ilike(search_term),
                    HCP.hospital_affiliation.ilike(search_term),
                )
            )

        # Count total matches
        count_query = select(func.count(HCP.id)).select_from(query.subquery())
        count_res = await db.execute(count_query)
        total_count = count_res.scalar() or 0

        # Fetch records
        query = query.order_by(HCP.decile.desc(), HCP.last_name.asc()).offset(offset).limit(limit)
        res = await db.execute(query)
        hcps = res.scalars().all()

        items = []
        for h in hcps:
            # Query recommendation if present
            rec_stmt = select(Recommendation).where(Recommendation.hcp_id == h.id).limit(1)
            rec_res = await db.execute(rec_stmt)
            rec = rec_res.scalar_one_or_none()

            items.append(
                HCPListItem(
                    id=h.id,
                    npi_synthetic=h.npi_synthetic,
                    first_name=h.first_name,
                    last_name=h.last_name,
                    specialty=h.specialty,
                    hospital_affiliation=h.hospital_affiliation,
                    city=h.city,
                    state=h.state,
                    territory_id=h.territory_id,
                    decile=h.decile,
                    digital_affinity=h.digital_affinity,
                    adoption_stage=h.adoption_stage,
                    priority_score=rec.propensity_score if rec else None,
                    priority_tier=rec.priority_tier if rec else "Unscored",
                    recommended_action=rec.recommended_action if rec else None,
                )
            )

        return items, total_count

    @staticmethod
    async def get_hcp_detail(db: AsyncSession, hcp_id: str) -> Optional[HCPDetailResponse]:
        hcp_stmt = select(HCP).where(HCP.id == hcp_id)
        hcp_res = await db.execute(hcp_stmt)
        hcp = hcp_res.scalar_one_or_none()
        if not hcp:
            return None

        # Fetch Rx
        rx_stmt = select(Prescription).where(Prescription.hcp_id == hcp_id).order_by(Prescription.month_year.asc())
        rx_res = await db.execute(rx_stmt)
        prescriptions = [
            PrescriptionPoint(
                month_year=r.month_year,
                trx_count=r.trx_count,
                nrx_count=r.nrx_count,
                competitor_trx_count=r.competitor_trx_count,
            )
            for r in rx_res.scalars().all()
        ]

        # Fetch Interactions
        int_stmt = select(Interaction).where(Interaction.hcp_id == hcp_id).order_by(Interaction.interaction_date.desc())
        int_res = await db.execute(int_stmt)
        interactions = [
            InteractionItem(
                id=i.id,
                interaction_date=i.interaction_date,
                channel=i.channel,
                rep_name=i.rep_name,
                topics_discussed=i.topics_discussed,
                sentiment=i.sentiment,
                notes=i.notes,
            )
            for i in int_res.scalars().all()
        ]

        # Fetch Recommendation
        rec_stmt = select(Recommendation).where(Recommendation.hcp_id == hcp_id).limit(1)
        rec_res = await db.execute(rec_stmt)
        rec = rec_res.scalar_one_or_none()

        hcp_item = HCPListItem(
            id=hcp.id,
            npi_synthetic=hcp.npi_synthetic,
            first_name=hcp.first_name,
            last_name=hcp.last_name,
            specialty=hcp.specialty,
            hospital_affiliation=hcp.hospital_affiliation,
            city=hcp.city,
            state=hcp.state,
            territory_id=hcp.territory_id,
            decile=hcp.decile,
            digital_affinity=hcp.digital_affinity,
            adoption_stage=hcp.adoption_stage,
            priority_score=rec.propensity_score if rec else None,
            priority_tier=rec.priority_tier if rec else "Unscored",
            recommended_action=rec.recommended_action if rec else None,
        )

        return HCPDetailResponse(
            hcp=hcp_item,
            prescriptions=prescriptions,
            interactions=interactions,
            top_drivers=rec.top_drivers if rec else None,
        )

hcp_service = HCPService()
