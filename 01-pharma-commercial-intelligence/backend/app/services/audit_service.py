import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog
from app.core.logging import correlation_id_ctx, logger

class AuditService:
    @staticmethod
    async def log_event(
        db: AsyncSession,
        user_id: str,
        user_role: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        Records an immutable audit event for compliance, model tracking, and governance.
        """
        audit_entry = AuditLog(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            user_id=user_id,
            user_role=user_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            correlation_id=correlation_id_ctx.get(),
            details=details,
        )
        db.add(audit_entry)
        try:
            await db.commit()
        except Exception as e:
            logger.error(f"Failed to persist audit log: {str(e)}")
            await db.rollback()
        return audit_entry

audit_service = AuditService()
