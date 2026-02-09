from datetime import datetime
from enum import Enum as PyEnum

from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import DateTime, text
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

uuid_pk = Annotated[
    UUID,
    mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
]

dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=dt_now_utc_sql)
]


class UserType(PyEnum):
    individual = "individual"   # физ. лицо
    legal = "legal"             # юр.  лицо