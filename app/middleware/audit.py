import logging
import time
from typing import Callable

from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.db.session import AsyncSessionLocal
from app.core.models.audit_log import AuditLog
from app.core.models.enums import AuditEventType
from app.core.models.user import User

logger = logging.getLogger(__name__)


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware that records each request into the AuditLog table.

    It is intentionally lightweight and uses a separate DB session so that
    audit writes do not interfere with request-level transactions.
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start = time.perf_counter()
        response: Response

        try:
            response = await call_next(request)
            event_type = AuditEventType.REQUEST
        except Exception:  # pragma: no cover - re-raise after logging
            response = Response(status_code=500)
            event_type = AuditEventType.ERROR
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000.0
            user_id_header = request.headers.get("X-User-Id")
            user_id = None

            # Validate user_id exists in database before logging
            if user_id_header and user_id_header.isdigit():
                try:
                    user_id_int = int(user_id_header)
                    async with AsyncSessionLocal() as session:
                        result = await session.execute(
                            select(User.id).where(User.id == user_id_int)
                        )
                        if result.scalar_one_or_none() is not None:
                            user_id = user_id_int
                except Exception:
                    # If validation fails, user_id remains None
                    pass

            try:
                async with AsyncSessionLocal() as session:
                    log = AuditLog(
                        user_id=user_id,
                        endpoint=request.url.path,
                        method=request.method,
                        status_code=response.status_code,
                        duration_ms=duration_ms,
                        event_type=event_type,
                    )
                    session.add(log)
                    await session.commit()
            except Exception as exc:  # Best-effort audit; never block response
                logger.warning("Audit log write failed: %s", exc, exc_info=True)

        return response



