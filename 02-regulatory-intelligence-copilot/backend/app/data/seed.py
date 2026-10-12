import asyncio
from sqlalchemy import select
from app.core.database import async_engine, AsyncSessionLocal, Base
from app.data.generator import generate_regulatory_dataset
from app.models.guidance import GuidanceDocument
from app.core.logging import logger

async def seed_database():
    logger.info("Initializing database schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        res = await session.execute(select(GuidanceDocument).limit(1))
        if res.scalar_one_or_none():
            logger.info("Regulatory database already contains records. Skipping initial seed.")
            return

        logger.info("Generating and seeding synthetic regulatory data...")
        dataset = generate_regulatory_dataset()

        session.add_all(dataset["users"])
        session.add_all(dataset["guidances"])
        session.add_all(dataset["sections"])
        session.add_all(dataset["diffs"])
        session.add_all(dataset["submissions"])

        await session.commit()
        logger.info(
            f"Successfully seeded: {len(dataset['users'])} users, {len(dataset['guidances'])} guidances, "
            f"{len(dataset['sections'])} sections, {len(dataset['diffs'])} diffs, {len(dataset['submissions'])} submission impacts."
        )

if __name__ == "__main__":
    asyncio.run(seed_database())
