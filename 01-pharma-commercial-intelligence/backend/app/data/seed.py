import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.core.database import async_engine, AsyncSessionLocal, Base
from app.data.generator import generate_synthetic_data

async def seed_database(num_hcps: int = 1000):
    """
    Creates tables and seeds synthetic demo data into the active database.
    """
    print(f"Connecting to database via async engine...")
    async with async_engine.begin() as conn:
        print("Creating tables if not present...")
        await conn.run_sync(Base.metadata.create_all)

    print("Generating synthetic records...")
    # Seed 1,000 for fast local demo initialization, configurable via CLI
    data = generate_synthetic_data(num_hcps=num_hcps)

    async with AsyncSessionLocal() as session:
        print("Saving records to database...")
        # Check if users already seeded
        from sqlalchemy import select
        from app.models.user import User
        existing = await session.execute(select(User).limit(1))
        if existing.scalar_one_or_none():
            print("Database already contains data, skipping seed.")
            return

        session.add_all(data["users"])
        session.add_all(data["territories"])
        session.add_all(data["products"])
        await session.commit()

        # Batch insert HCPs & dependencies in chunks for performance
        chunk_size = 500
        for i in range(0, len(data["hcps"]), chunk_size):
            session.add_all(data["hcps"][i:i+chunk_size])
            await session.commit()
            print(f"Seeded HCPs {i} to {min(i+chunk_size, len(data['hcps']))}...")

        for i in range(0, len(data["prescriptions"]), chunk_size * 2):
            session.add_all(data["prescriptions"][i:i+chunk_size*2])
            await session.commit()

        for i in range(0, len(data["interactions"]), chunk_size):
            session.add_all(data["interactions"][i:i+chunk_size])
            await session.commit()

        for i in range(0, len(data["recommendations"]), chunk_size):
            session.add_all(data["recommendations"][i:i+chunk_size])
            await session.commit()

        print("Database successfully seeded with synthetic commercial data!")

if __name__ == "__main__":
    count = 1000
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    asyncio.run(seed_database(num_hcps=count))
