from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


Database = Annotated[Session, Depends(get_db)]
ResourceId = Annotated[int, Path(ge=-(2**63), le=2**63 - 1)]
