import time
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recommendation import Recommendation
from app.models.hcp import HCP
from app.models.product import Product
from app.schemas.recommendation import RecommendationItem, BatchGenerateResponse
from app.ml.features import compute_hcp_features
from app.ml.model import propensity_engine
from app.ml.nba_rules import evaluate_nba_decision
from app.ai.agents.tools import fetch_hcp_prescriptions, fetch_hcp_interactions

class RecommendationService:
    @staticmethod
    async def list_recommendations(
        db: AsyncSession,
        territory_id: Optional[str] = None,
        priority_tier: Optional[str] = None,
        specialty: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[RecommendationItem]:
        query = select(Recommendation, HCP, Product).join(HCP, Recommendation.hcp_id == HCP.id).join(Product, Recommendation.product_id == Product.id)

        if territory_id:
            query = query.where(HCP.territory_id == territory_id)
        if priority_tier:
            query = query.where(Recommendation.priority_tier == priority_tier)
        if specialty:
            query = query.where(HCP.specialty == specialty)

        query = query.order_by(desc(Recommendation.propensity_score)).offset(offset).limit(limit)
        res = await db.execute(query)
        rows = res.all()

        items = []
        for rec, hcp, prod in rows:
            items.append(
                RecommendationItem(
                    id=rec.id,
                    hcp_id=hcp.id,
                    hcp_name=f"Dr. {hcp.first_name} {hcp.last_name}",
                    specialty=hcp.specialty,
                    territory_id=hcp.territory_id,
                    product_name=prod.name,
                    propensity_score=rec.propensity_score,
                    priority_tier=rec.priority_tier,
                    recommended_action=rec.recommended_action,
                    recommended_channel=rec.recommended_channel,
                    top_drivers=rec.top_drivers,
                    model_version=rec.model_version,
                    status=rec.status,
                    generated_at=rec.created_at,
                )
            )
        return items

    @staticmethod
    async def generate_batch_recommendations(
        db: AsyncSession,
        batch_limit: int = 500
    ) -> BatchGenerateResponse:
        start_time = time.perf_counter()

        # Query HCPs to score
        hcp_stmt = select(HCP).limit(batch_limit)
        res = await db.execute(hcp_stmt)
        hcps = res.scalars().all()

        count = 0
        for hcp in hcps:
            rx_list = await fetch_hcp_prescriptions(db, hcp.id)
            inter_list = await fetch_hcp_interactions(db, hcp.id)

            features = compute_hcp_features(
                hcp_decile=hcp.decile,
                digital_affinity=hcp.digital_affinity,
                prescriptions=rx_list,
                interactions=inter_list,
            )
            score, drivers = propensity_engine.predict_propensity(features)
            tier, action, channel = evaluate_nba_decision(score, features)

            # Match product
            prod_id = "PROD-ONCO-01" if hcp.specialty in ["Oncology", "Hematology"] else (
                "PROD-CARD-02" if hcp.specialty == "Cardiology" else "PROD-ENDO-03"
            )

            # Upsert recommendation
            rec_stmt = select(Recommendation).where(Recommendation.hcp_id == hcp.id)
            rec_res = await db.execute(rec_stmt)
            existing_rec = rec_res.scalar_one_or_none()

            if existing_rec:
                existing_rec.propensity_score = score
                existing_rec.priority_tier = tier
                existing_rec.recommended_action = action
                existing_rec.recommended_channel = channel
                existing_rec.top_drivers = drivers
                existing_rec.model_version = "xgb-v1.0"
            else:
                new_rec = Recommendation(
                    id=f"REC-{hcp.id}",
                    hcp_id=hcp.id,
                    product_id=prod_id,
                    propensity_score=score,
                    priority_tier=tier,
                    recommended_action=action,
                    recommended_channel=channel,
                    top_drivers=drivers,
                    model_version="xgb-v1.0",
                    status="PENDING",
                )
                db.add(new_rec)
            count += 1

        await db.commit()
        duration = time.perf_counter() - start_time

        return BatchGenerateResponse(
            total_processed=len(hcps),
            recommendations_generated=count,
            model_version="xgb-v1.0",
            execution_time_seconds=round(duration, 2),
        )

recommendation_service = RecommendationService()
