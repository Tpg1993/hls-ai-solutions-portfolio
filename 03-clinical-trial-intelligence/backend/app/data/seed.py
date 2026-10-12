import asyncio
from sqlalchemy import select
from app.core.database import async_engine, AsyncSessionLocal, Base
from app.data.generator import generate_clinical_trials_dataset
from app.models.trial import ClinicalTrial
from app.core.logging import logger

async def seed_database():
    logger.info("Initializing clinical trials database schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(ClinicalTrial).limit(1))
        if res.scalar_one_or_none():
            logger.info("Clinical trials database already contains records. Skipping seed.")
            return

        logger.info("Generating and seeding clinical trials, patients, and operational site records...")
        dataset = generate_clinical_trials_dataset()

        session.add_all(dataset["users"])
        session.add_all(dataset["trials"])
        session.add_all(dataset["criteria"])
        session.add_all(dataset["sites"])
        session.add_all(dataset["site_metrics"])
        session.add_all(dataset["patients"])
        session.add_all(dataset["biomarkers"])
        session.add_all(dataset["labs"])
        session.add_all(dataset["matches"])

        await session.commit()
        logger.info(
            f"Successfully seeded: {len(dataset['users'])} users, {len(dataset['trials'])} trials, "
            f"{len(dataset['criteria'])} criteria, {len(dataset['sites'])} sites, {len(dataset['patients'])} patients, "
            f"{len(dataset['matches'])} patient-trial matches."
        )

if __name__ == "__main__":
    asyncio.run(seed_database())
