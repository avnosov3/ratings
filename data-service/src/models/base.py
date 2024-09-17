from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

CASCADE = "CASCADE"
ALL_DELETE = "all, delete"
SET_NULL = "SET NULL"


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(POSTGRES_UUID, primary_key=True, default=uuid4)
