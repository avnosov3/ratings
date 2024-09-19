from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ALL_DELETE, Base

if TYPE_CHECKING:
    from .review import Review

USER_NAME_LEN = 512
USER_EMAIL_LEN = 512
USER_IPADDRES_LEN = 64


class User(Base):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(
        String(USER_NAME_LEN),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(USER_EMAIL_LEN),
        unique=True,
        nullable=False,
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(USER_IPADDRES_LEN),
        nullable=True,
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
        cascade=ALL_DELETE,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id} email={self.email})"
